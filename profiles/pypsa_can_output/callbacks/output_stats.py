import dash
from dash import Output, Input, State, ALL, dcc

from profiles.pypsa_can_output.visualization_scripts.output_stats import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'pypsa_can_output',
            'viz': 'output_stats'
        }, 'figure'),

        Output({
            'type': 'pypsa_can_output-output_stats-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'pypsa_can_output-output_stats-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pypsa_can_output-output_stats-download-button',
            'index': ALL
        }, 'n_clicks'),
        Input({
            'type': 'pypsa_can_output-output_stats-scenario-select',
            'index': ALL
        }, 'value'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'pypsa_can_output',
            'viz': 'output_stats'
        }, 'figure'),

        State({
            'type': 'pypsa_can_output-output_stats-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_output_stats(_years, _download, _scenarios, _canvas, _data):
        #print('updating output_stats plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'pypsa_can_output-output_stats-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'pypsa_can_output-output_stats-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['PyPSA_CAN']['Output Stats'].to_csv,
                                             "output_stats.csv")
            return _canvas, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'pypsa_can_output-output_stats-plot-select')):
                idx = i
                break

        df = data_handler.processed_data['PyPSA_CAN']['Output Stats']
        _canvas[idx] = render_plot(df, _years[idx], _scenarios[idx])


        return _canvas, [dash.no_update for _ in _data]
