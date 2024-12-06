import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from components import ids
from profiles.macromodel.visualization_scripts import economy, households, labour_market

render_func = {
    'economy': economy.render_plot,
    'households': households.render_plot,
    'labour_market': labour_market.render_plot
}

name_mapping = {
    'economy' : 'Economy',
    'households': 'Households',
    'labour_market': 'Labour Market'
}

def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile':MATCH,
            'name': MATCH
        }, 'figure', allow_duplicate=True),
        Output({
            'type': 'sectored-region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'sectored-year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'sectored-download',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        Output({
            'type': 'sectored-scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'sectored-scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'sectored-unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output(
            {
                'type': 'sectored-pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'sectored-text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Input({
            'type': 'sectored-plot-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'sectored-aggregate-switch',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'checked'),
        Input({
            'type': 'sectored-scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'sectored-scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'sectored-sector-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'sectored-region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'sectored-year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
         Input({
            'type': 'sectored-unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input(
            {
                'type': 'sectored-pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'sectored-text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'sectored-download-button',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'n_clicks'),
        State({
            'type': 'sectored-region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'sectored-year-select',
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
            'type': 'sectored-download',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        State({
            'type': 'sectored-scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'sectored-scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'sectored-unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State(
            {
                'type': 'sectored-pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'sectored-text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _aggregates, _scenarios, _scenario, _sectors, _regions, _years, _units, _pattern, _text,
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
                                           pattern_active=_pattern[idx], text_active=_text[idx], sector=_sectors[idx])

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
                                           _years[idx], scenario=_scenario[idx], sector=_sectors[idx])
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
                                           _years[idx], scenario=_scenario[idx], sector=_sectors[idx])

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
                                           _years[idx], scenario=_scenario[idx], sector=_sectors[idx])

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
                                           pattern_active=_pattern[idx], text_active=_text[idx], sector=_sectors[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in
                                             _data], _s_style, _m_style, _u_style, _pattern_style, _text_style