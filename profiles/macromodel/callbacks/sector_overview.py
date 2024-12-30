import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from components import ids
from profiles.macromodel.visualization_scripts import sector_overview

render_func = {
    'sector_overview': sector_overview.render_plot
}

name_mapping = {
    'sector_overview' : 'Sector Overview'
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
            'type': 'so-region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-download',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        Output({
            'type': 'so-scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-vartype-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output(
            {
                'type': 'so-pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'so-text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Input({
            'type': 'so-plot-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-aggregate-switch',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'checked'),
        Input({
            'type': 'so-scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-year-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-vartype-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input(
            {
                'type': 'so-pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'so-text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'so-download-button',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'n_clicks'),
        State({
            'type': 'so-region-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-year-select',
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
            'type': 'so-download',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        State({
            'type': 'so-scenario-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-scenario-multi-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-unit-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-vartype-select',
            'index': ALL,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State(
            {
                'type': 'so-pattern-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'so-text-switch',
                'index': ALL,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _units, _vartypes, _pattern, _text,
                           _download, _r_style, _y_style, _canvas, _data, _s_style, _m_style, _u_style, _v_style, _pattern_style,
                           _text_style):
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = 'Macromodel'
        name = name_mapping.get(trigger_id['name'])
        print(f'updating sector_overview {name}, {model} plot')
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
            return _canvas, _r_style, _y_style, _s_style, _m_style, _u_style, _v_style, _pattern_style, _text_style

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
            _v_style[idx] = {'display': 'block'}
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
                                           _vartypes[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _v_style[idx] = {'display': 'block'}
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
                                           _vartypes[idx],
                                           _years[idx], scenario=_scenario[idx])
        elif _p_type[idx] == 'Trend in one Year':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _v_style[idx] = {'display': 'block'}
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
                                           _vartypes[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _v_style[idx] = {'display': 'block'}
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
                                           _vartypes[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _v_style[idx] = {'display': 'block'}
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
                                           _vartypes[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in
                                             _data], _s_style, _m_style, _u_style, _v_style, _pattern_style, _text_style