import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.generation_capacity import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'gencap'
        }, 'figure'),
        Output({
            'type': 'energy_model-gencap-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-gencap-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output(
            {
                'type': 'energy_model-gencap-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'energy_model-gencap-text-switch',
                'index': ALL
            },
            'style'
        ),
        Input({
            'type': 'energy_model-gencap-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'energy_model-gencap-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap-year-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-gencap-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'energy_model-gencap-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'energy_model-gencap-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'energy_model-gencap-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-gencap-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'gencap'
        }, 'figure'),
        State({
            'type': 'energy_model-gencap-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-gencap-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-gencap-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'energy_model-gencap-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'energy_model-gencap-text-switch',
                'index': ALL
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _pattern, _text,
                         _download,_r_style, _y_style, _canvas, _data, _s_style, _m_style, _pattern_style, _text_style):
        print('updating gencap plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-gencap-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-gencap-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Capacity'].to_csv, "gencap.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-gencap-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['Power System Models']['Capacity'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'} 
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['Power System Models']['Capacity'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'} 
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['Power System Models']['Capacity'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['Power System Models']['Capacity'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data], _s_style, _m_style, _pattern_style, _text_style
