import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.output_stats import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Output Stats'
        }, 'figure'),

        Output({
            'type': 'energy_model-output_stats-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-output_stats-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-output_stats-download-button',
            'index': ALL
        }, 'n_clicks'),
        Input({
            'type': 'energy_model-output_stats-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-output_stats-scenario-group-select',
            'index': ALL
        }, 'value'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Output Stats'
        }, 'figure'),

        State({
            'type': 'energy_model-output_stats-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_output_stats(_years, _download, _scenarios, _scenario_group, _canvas, _data):
        #print('updating output_stats plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-output_stats-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-output_stats-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Output Stats'].to_csv,
                                             "output_stats.csv")
            return _canvas, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-output_stats-plot-select')):
                idx = i
                break

        df = data_handler.processed_data['Power System Models']['Output Stats']
        if _scenario_group[idx] != 'ALL':
            df = df[df['scenario'].str.contains(_scenario_group[idx])]
            scenarios = df['scenario'].unique().tolist()

            _scenarios[idx] = list(set(_scenarios[idx] + scenarios))



        _canvas[idx] = render_plot(df, _years[idx], _scenarios[idx])


        return _canvas, [dash.no_update for _ in _data]
