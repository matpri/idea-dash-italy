import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from components import ids
from utils.generic_profile.visualization_scripts.generic_viz import render_plot


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'model':MATCH,
            'name': MATCH
        }, 'figure'),
        Output({
            'type': 'generic-region-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'generic-year-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'generic-download',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'data'),
        Output({
            'type': 'generic-scenario-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'generic-scenario-multi-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'generic-unit-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        Output(
            {
                'type': 'generic-pattern-switch',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'generic-text-switch',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Input({
            'type': 'generic-plot-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'generic-aggregate-switch',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'checked'),
        Input({
            'type': 'generic-scenario-multi-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'generic-scenario-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'generic-region-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'generic-year-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
         Input({
            'type': 'generic-unit-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        Input(
            {
                'type': 'generic-pattern-switch',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'generic-text-switch',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'generic-download-button',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'n_clicks'),
        State({
            'type': 'generic-region-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'generic-year-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'figure'),
        State({
            'type': 'generic-download',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'data'),
        State({
            'type': 'generic-scenario-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'generic-scenario-multi-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'generic-unit-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'style'),
        State(
            {
                'type': 'generic-pattern-switch',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'generic-text-switch',
                'index': ALL,
                'model': MATCH,
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
        model = trigger_id['model']
        name = trigger_id['name']
        print(f'updating {name}, {model} plot')

        if 'generic-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'generic-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _u_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'generic-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])
        profile = data_handler.profiles[model]
        patterns = [profile.pattern_from_key(key) for key in _scenarios[idx]]
        print('patterns:', patterns)

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
                                           pattern_active=_pattern[idx], text_active=_text[idx], pattern_list=patterns)

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
                                           _years[idx], scenario=_scenario[idx], pattern_list=patterns)
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
                                           _years[idx], scenario=_scenario[idx], pattern_list=patterns)

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
                                           _years[idx], scenario=_scenario[idx], pattern_list=patterns)

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
                                           pattern_active=_pattern[idx], text_active=_text[idx], pattern_list=patterns)

        return _canvas, _r_style, _y_style, [dash.no_update for _ in
                                             _data], _s_style, _m_style, _u_style, _pattern_style, _text_style