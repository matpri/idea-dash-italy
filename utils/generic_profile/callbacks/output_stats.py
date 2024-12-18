import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from components import ids
from utils.generic_profile.visualization_scripts.output_stats import render_plot


def link(app):
    print('linking output_stats')

    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'figure'),
        Output({
            'type': 'download',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'data'),
        Input({
            'type': 'plot-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'value'),
        Input({
            'type': 'scenario-group-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'value'),
        Input({
            'type': 'year-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'value'),
        Input({
            'type': 'scenario-select',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'value'),
        Input({
            'type': 'download-button',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'figure'),
        State({
            'type': 'download',
            'index': ALL,
            'model': MATCH,
            'viz': 'output_stats'
        }, 'data'),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _scen_group, _years, _scenarios, _download, _canvas, _data):
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = trigger_id['model']
        name = 'Output Stats'
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
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if (id['id']['index'] == trigger_id['index']):
                idx = i
                break

        df = data_handler.processed_data[model][name].copy()
        if _scen_group is not None:
            if len(_scen_group) > 0:
                if _scen_group[idx] != 'ALL':
                    df = df[(df['base_scenario'] == _scen_group[idx]) | (df.scenario.isin(_scenarios[idx]))]
                else:
                    df = df[df.scenario.isin(_scenarios[idx])]
            else:
                df = df[df.scenario.isin(_scenarios[idx])]
        else:
            df = df[df.scenario.isin(_scenarios[idx])]

        print('idx:', idx, 'plot type:', _years[idx])
        _canvas[idx] = render_plot(
            _p_type[idx],
            df,
            _years[idx],
            model
        )

        return _canvas, [dash.no_update for _ in
                         _data],
