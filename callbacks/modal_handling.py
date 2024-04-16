import dash
from dash import html, Input, Output, State

from components import ids


def link(app):
    @app.callback(
        Output({'type': 'modal', 'index': dash.dependencies.ALL}, 'opened'),
        Output(ids.DATA_CHANGE, 'n_clicks'),
        Input({'type': 'open-modal', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input({'type': 'modal-close-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input({'type': 'modal-submit-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
        State({'type': 'modal', 'index': dash.dependencies.ALL}, 'opened'),
        State({'type': 'upload-chip-group', 'file': dash.dependencies.ALL, 'profile': dash.dependencies.ALL}, 'value'),
        State(ids.DATA_CHANGE, 'n_clicks'),
        State({'type': 'upload-scenario-name', 'file': dash.dependencies.ALL}, 'value'),
        prevent_initial_call=True,
    )
    def handle_modals(
            open_clicks, close_clicks, submit_clicks, opened_modals, selected_chips, n_clicks, scenario_names
    ):
        print('handle_modals', open_clicks, close_clicks, submit_clicks, opened_modals, selected_chips, n_clicks, scenario_names)
        if not any([open_clicks, close_clicks, submit_clicks]):
            return dash.no_update, dash.no_update

        # get triggered input info
        ctx = dash.callback_context
        triggered_input = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        triggered_value = ctx.triggered[0]['value']
        if triggered_value is None:
            return dash.no_update
        output = [False] * len(ctx.outputs_list[0])

        # set flag based on button type
        open_flag = triggered_input['type'] == 'open-modal'
        if triggered_input['type'] in ['modal-close-button', 'modal-submit-button']:
            print(f"{'Submitting data' if triggered_input['type'] == 'modal-submit-button' else 'Closing data modal'}")

        # special case for 'data' index
        if triggered_input['index'] == 'data':
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == 'data':
                    output[i] = open_flag

            if triggered_input['type'] == 'modal-submit-button':
                from main import data_handler
                for i, ls in enumerate(ctx.states_list[1]):
                    chip = ls['id']
                    file = chip['file']
                    scenarios = ctx.states_list[3]
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
                    return output, 1
                else:
                    return output, n_clicks + 1
            return output, dash.no_update

        # general case for 'selected' index
        if triggered_input['index'].startswith('selected'):
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == triggered_input['index']:
                    output[i] = open_flag
                elif out['id']['index'] == 'data':
                    output[i] = True
            return output, dash.no_update

        if triggered_input['index'] == 'help':
            print('help')
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == triggered_input['index']:
                    output[i] = open_flag
            return output, dash.no_update

        return dash.no_update
