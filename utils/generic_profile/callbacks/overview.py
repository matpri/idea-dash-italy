import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from components import ids
from utils.generic_profile.visualization_scripts.overview import render_plot


def link(app):
    print('linking overview')

    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'figure'),
        Output({
            'type': 'download',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'data'),
        Output({
            'type': 'unit-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'data'),
        Output({
            'type': 'unit-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'value'),
        Input({
            'type': 'plot-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'value'),
        Input({
            'type': 'scenario-group-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'value'),
        Input({
            'type': 'unit-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'value'),
        Input({
            'type': 'download-button',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'figure'),
        State({
            'type': 'unit-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'data'),
        State({
            'type': 'download',
            'index': ALL,
            'model': MATCH,
            'viz': 'overview'
        }, 'data'),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _scenarios, _unit, _download, _canvas, _u_data, _data):
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = trigger_id['model']
        name = 'Overview'
        print(f'updating {name}, {model} plot')

        if 'download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _data, _u_data, _unit

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'plot-select')):
                idx = i
                df = data_handler.processed_data[model][name]
                _u_data[idx] = [{'label': unit, 'value': unit} for unit in
                                df[df['variable'] == _p_type[idx]]['unit'].unique().tolist()]
                break
        if not trigger_id['type'] == 'unit-select':
            _unit[idx] = _u_data[idx][0]['value']

        df = data_handler.processed_data[model][name].copy()
        if _scenarios is not None:
            if _scenarios[idx] != 'ALL':
                df = df[df['base_scenario'] == _scenarios[idx]]

        print('idx:', idx, 'plot type:', _p_type[idx])
        _canvas[idx] = render_plot(_p_type[idx],
                                   df,
                                   _unit[idx]
                                   )

        return _canvas, [dash.no_update for _ in
                         _data], _u_data, _unit
