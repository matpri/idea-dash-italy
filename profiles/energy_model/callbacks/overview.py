import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.overview import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'overview'
        }, 'figure'),

        Output({
            'type': 'energy_model-overview-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-overview-fill-switch',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'energy_model-overview-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-overview-groupby-toggle',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-overview-region-toggle',
                'index': ALL
            }, 'value'
        ),
        Input(
            {
                'type': 'energy_model-overview-fill-switch',
                'index': ALL,
            }, 'checked'

        ),
        Input({
            'type': 'energy_model-overview-scenario-group-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'energy_model-overview-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'overview'
        }, 'figure'),

        State({
            'type': 'energy_model-overview-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-overview-fill-switch',
            'index': ALL
        }, 'style'),

        prevent_initial_call=True
    )
    def update_overview(_p_type, _groupby, _region, _fill, _scenarios, _download, _canvas, _data, _fillswitch):
        #print('updating overview plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-overview-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-overview-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Overview'].to_csv,
                                             "overview.csv")
            return _canvas, _data, _fillswitch

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-overview-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])
        _groupby_model = _groupby[idx] == 1
        _groupby_scenario = _groupby[idx] == 2
        _groupby_version = _groupby[idx] == 3

        df = data_handler.processed_data['Power System Models']['Overview']
        if _scenarios[idx] != 'ALL':
            df = df[df['scenario'].str.contains(_scenarios[idx])]

        _canvas[idx] = render_plot(_p_type[idx], df,
                                   _groupby_model, _groupby_scenario, _groupby_version, _region[idx]=='CAN', _fill[idx])

        _fillswitch[idx] = {'display': 'none'}
        if _groupby[idx] > 0:
            _fillswitch[idx] = {'display': 'block'}

        return _canvas, [dash.no_update for _ in _data], _fillswitch
