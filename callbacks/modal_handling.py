import dash
from dash import Input, Output, State

from components import ids


def link(app):
    """
    Link the modal handling callbacks to the Dash app.

    This module handles the opening, closing, and submission of modals
    in the Dash application. It manages the state of multiple modals
    and updates the relevant outputs based on user interactions.

    Parameters:
    - app: The Dash application instance.
    """
    @app.callback(
        Output({'type': ids.MODAL, 'index': dash.dependencies.ALL}, 'opened'),
        Output(ids.DATA_CHANGE, 'n_clicks'),
        Output(ids.UPDATE_CHIPS, 'n_clicks'),
        Input({'type': ids.OPEN_MODAL, 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input({'type': ids.MODAL_CLOSE_BUTTON, 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input({'type': ids.MODAL_SUBMIT_BUTTON, 'index': dash.dependencies.ALL}, 'n_clicks'),
        State({'type': ids.MODAL, 'index': dash.dependencies.ALL}, 'opened'),
        State({'type': ids.UPLOAD_CHIP_GROUP, 'file': dash.dependencies.ALL, 'profile': dash.dependencies.ALL}, 'value'),
        State(ids.DATA_CHANGE, 'n_clicks'),
        State(ids.UPDATE_CHIPS, 'n_clicks'),
        State({'type':  ids.UPLOAD_SCENARIO_NAME, 'file': dash.dependencies.ALL}, 'value'),
        prevent_initial_call=True,
    )
    def handle_modals(
            open_clicks, close_clicks, submit_clicks, opened_modals, selected_chips, n_clicks, _update_chips, scenario_names
    ):
        """
        Handle the opening, closing, and submission of modals.

        This function is triggered by clicks on buttons that effect modals and updates
        the state of the modals accordingly. It also processes data when
        the submit button is clicked.
        ids.DATA_CHANGE and ids.UPDATE_CHIPS are hidden buttons that we manually trigger to call callbacks when we want data is updated, e.g. to rerender plots

        Parameters:
        - open_clicks: List of clicks on open modal buttons.
        - close_clicks: List of clicks on close modal buttons.
        - submit_clicks: List of clicks on submit buttons.
        - opened_modals: Current state of opened modals.
        - selected_chips: Selected chips from the upload chip groups.
        - n_clicks: Number of clicks on the data change button.
        - _update_chips: Number of clicks on the update chips button.
        - scenario_names: Names of the scenarios entered by the user.

        Returns:
        - A tuple containing the updated state of modals and click counts.
        """
        print('handle_modals', open_clicks, close_clicks, submit_clicks, opened_modals, selected_chips, n_clicks, scenario_names)
        if not any([open_clicks, close_clicks, submit_clicks]):
            return dash.no_update, dash.no_update, dash.no_update

        # get triggered input info
        ctx = dash.callback_context
        triggered_input = eval(ctx.triggered[0]['prop_id'].split('.')[0]) if ctx.triggered[0]['prop_id'].count('.') < 2 else '.'.join(ctx.triggered[0]['prop_id'].split('.')[:-1])
        triggered_value = ctx.triggered[0]['value']
        if triggered_value is None:
            return dash.no_update
        output = [False] * len(ctx.outputs_list[0])

        # set flag based on button type
        open_flag = triggered_input['type'] == ids.OPEN_MODAL
        if triggered_input['type'] in ['modal-close-button', 'modal-submit-button']:
            print(f"{'Submitting data' if triggered_input['type'] == 'modal-submit-button' else 'Closing data modal'}")

        # special case for 'data' index
        if triggered_input['index'] == 'data':
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == 'data':
                    output[i] = open_flag

            if triggered_input['type'] == 'modal-submit-button':
                from utils.data_state import data_handler
                for i, ls in enumerate(ctx.states_list[1]):
                    chip = ls['id']
                    file = chip['file']
                    scenarios = ctx.states_list[4]
                    scenario = None
                    for s in scenarios:
                        if s['id']['file'] == file:
                            scenario = s['value']
                            break
                    data_handler.data[file]['selected'][chip['profile']] = selected_chips[i]
                    data_handler.data[file]['scenario'] = scenario if scenario is not None else file
                print(data_handler)
                data_handler.process_data()
                if n_clicks is None:
                    return output, 1, 1
                else:
                    return output, n_clicks + 1, _update_chips + 1
            return output, dash.no_update, dash.no_update

        # general case for 'selected' index
        if triggered_input['index'].startswith('selected'):
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == triggered_input['index']:
                    output[i] = open_flag
                elif out['id']['index'] == 'data':
                    output[i] = True
            return output, dash.no_update, dash.no_update

        if triggered_input['index'] == 'help':
            print('help')
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == triggered_input['index']:
                    output[i] = open_flag
            return output, dash.no_update, dash.no_update

        return dash.no_update
