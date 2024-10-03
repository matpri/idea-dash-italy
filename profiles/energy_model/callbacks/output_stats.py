import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.output_stats import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'output_stats'
        }, 'figure'),

        Output({
            'type': 'energy_model-output_stats-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-output_stats-fill-switch',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'energy_model-output_stats-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-output_stats-groupby-toggle',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-output_stats-region-toggle',
                'index': ALL
            }, 'value'
        ),
        Input(
            {
                'type': 'energy_model-output_stats-fill-switch',
                'index': ALL,
            }, 'checked'

        ),
        Input({
            'type': 'energy_model-output_stats-scenario-group-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'energy_model-output_stats-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'output_stats'
        }, 'figure'),

        State({
            'type': 'energy_model-output_stats-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-output_stats-fill-switch',
            'index': ALL
        }, 'style'),

        prevent_initial_call=True
    )
    def update_output_stats(_p_type, _groupby, _region, _fill, _scenarios, _download, _canvas, _data, _fillswitch):
        #print('updating output_stats plot')
        from main import data_handler
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
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-output_stats-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])
        _groupby_model = _groupby[idx] == 1
        _groupby_scenario = _groupby[idx] == 2
        _groupby_version = _groupby[idx] == 3

        df = data_handler.processed_data['Power System Models']['Output Stats']
        if _scenarios[idx] != 'ALL':
            df = df[df['scenario'].str.contains(_scenarios[idx])]

        _canvas[idx] = render_plot(_p_type[idx], df,
                                   _groupby_model, _groupby_scenario, _groupby_version, _region[idx]=='CAN', _fill[idx])

        _fillswitch[idx] = {'display': 'none'}
        if _groupby[idx] > 0:
            _fillswitch[idx] = {'display': 'block'}

        return _canvas, [dash.no_update for _ in _data], _fillswitch
