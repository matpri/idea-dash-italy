import dash
from dash import Output, Input, State, MATCH, dcc, MATCH
from profiles.macromodel.visualization_scripts.histogram import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': MATCH,
            'name': 'Histograms'
        }, 'figure', allow_duplicate=True),
        Output({
            'type': 'download',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'data'),
        Output({
            'type': 'unit-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Output({
            'type': 'unit-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'data'),
        Output({
            'type': 'variable-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Output({
            'type': 'variable-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'data'),
        Input({
            'type': 'plot-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Input({
            'type': 'scenario-multi-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Input({
            'type': 'variable-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),

        Input({
            'type': 'region-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Input({
            'type': 'year-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Input({
            'type': 'unit-select',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Input({
            'type': 'bins-slider',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'value'),
        Input({
            'type': 'download-button',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'n_clicks'),

        State({
            'type': 'download',
            'index': MATCH,
            'profile': MATCH,
            'viz_type': 'Histograms'
        }, 'data'),

        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _scenarios, _variable, _regions, _years, _units, _nbins,
                           _download, _data):
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = ctx.triggered_id
        model = 'Macromodel'
        name = 'Histograms'
        _canvas = dash.no_update
        variables = dash.no_update
        units = dash.no_update

        if 'download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _data, _units, units, _variable, variables

        if 'plot-select' in trigger_id['type']:
            df = data_handler.processed_data[model][name]
            df_scen = df[df['scenario'].isin(_scenarios) & (df['region'] == _regions) & (df['time'] == _years) &
                         (df['type'] == _p_type)]
            variables = df_scen['variable'].unique().tolist()
            _variable = variables[0]
            df_scen = df_scen[df_scen['variable'] == _variable]
            units = df_scen['unit'].unique().tolist()
            _units = units[0]

        if 'variable-select' in trigger_id['type']:
            df = data_handler.processed_data[model][name]
            df_scen = df[df['scenario'].isin(_scenarios) & (df['region'] == _regions) &( df['time'] == _years) &
                         (df['type'] == _p_type)]
            df_scen = df_scen[df_scen['variable'] == _variable]
            units = df_scen['unit'].unique().tolist()
            _units = units[0]

        print('plot type:', _p_type)

        _canvas = render_plot(_p_type, data_handler.processed_data[model][name],
                              _scenarios, _regions, _units, _years, _variable, n_bins=_nbins)

        return _canvas, dash.no_update, _units, units, _variable, variables
