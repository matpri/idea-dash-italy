import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from components import ids
from profiles.macromodel.visualization_scripts import financial_markets, government, economy, households, labour_market

render_func = {
    'central_government': government.render_plot,
    'financial_markets': financial_markets.render_plot,
    'labour_market': labour_market.render_plot,
    'households': households.render_plot,
    'economy': economy.render_plot
}

name_mapping = {
    'government': 'Government',
    'financial_markets': 'Financial Markets',
    'labour_market': 'Labour Market',
    'households': 'Households',
    'economy': 'Economy Overview'
}

def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile':MATCH,
            'name': MATCH
        }, 'figure'),
        Output({
            'type': 'region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'download',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        Output({
            'type': 'scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output(
            {
                'type': 'pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Input({
            'type': 'plot-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'aggregate-switch',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'checked'),
        Input({
            'type': 'scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
         Input({
            'type': 'unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input(
            {
                'type': 'pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'download-button',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'n_clicks'),
        State({
            'type': 'region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'figure'),
        State({
            'type': 'download',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        State({
            'type': 'scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State(
            {
                'type': 'pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _units, _pattern, _text,
                           _download, _r_style, _y_style, _canvas, _data, _s_style, _m_style, _u_style, _pattern_style,
                           _text_style):
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = 'Macromodel'
        name = name_mapping.get(trigger_id['name'])
        print(f'updating {name}, {model} plot')
        render_plot = render_func[trigger_id['name']]

        if 'download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _u_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])
        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _units[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _units[idx],
                                           _years[idx], scenario=_scenario[idx])
        elif _p_type[idx] == 'Trend in one Year':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend in one Year',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _units[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _units[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _units[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in
                                             _data], _s_style, _m_style, _u_style, _pattern_style, _text_style