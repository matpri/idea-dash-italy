import dash
from dash import Output, Input, State, ALL, dcc

from profiles.cims_output.visualization_scripts.inputs import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'cims_output',
            'viz': 'inputs'
        }, 'figure'),
        Output({
            'type': 'cims-inputs-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'cims-inputs-cost-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'cims-inputs-policy-widget',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'cims-inputs-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-inputs-cost-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-inputs-cost-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-inputs-cost-region-select',
            'index': ALL
        }, 'value'),Input({
            'type': 'cims-inputs-cost-sector-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-inputs-policy-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-inputs-policy-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-inputs-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'cims_output',
            'viz': 'inputs'
        }, 'figure'),
        State({
            'type': 'cims-inputs-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'cims-inputs-cost-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'cims-inputs-policy-widget',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_inputs(_p_type,
                      _c_select, _c_scenario, _c_region, _c_sector,
                      _policy_scenarios, _policy_region,
                      _download, _canvas, _data,  _cost_style, _policy_style
                      ):
        # Importing the data handler for processing data
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        # Handling download button click
        if 'cims-inputs-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'cims-inputs-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['CIMS']['Inputs'].to_csv,
                                             "inputs.csv")
            return (
                _canvas, _data, _cost_style, _policy_style
            )

        # Determine the index of the plot select input
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'cims-inputs-plot-select')):
                idx = i
                break

        if 'Cost' in _p_type[idx] and not 'Transmission Costs' in _p_type[idx]:
            _cost_style[idx] = {'display': 'block'}
            _policy_style[idx] = {'display': 'none'}
        elif 'Policy' in _p_type[idx]:
            _cost_style[idx] = {'display': 'none'}
            _policy_style[idx] = {'display': 'block'}

        # Render the plot based on the selected inputs
        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['CIMS']['Inputs'],_c_type=_c_select[idx], _c_scenario=_c_scenario[idx], _c_region=_c_region[idx], _c_sector=_c_sector[idx], _policy_scenarios=_policy_scenarios[idx], _policy_region=_policy_region[idx])


        return (_canvas, [dash.no_update for _ in
                          _data],_cost_style, _policy_style
                )
