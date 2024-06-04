import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.cost_gencap import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'gencap_cost'
        }, 'figure'),
        Output({
            'type': 'energy_model-gencap_cost-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap_cost-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap_cost-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-gencap_cost-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap_cost-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-gencap_cost-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output(
            {
                'type': 'energy_model-gencap_cost-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'energy_model-gencap_cost-text-switch',
                'index': ALL
            },
            'style'
        ),
        Input({
            'type': 'energy_model-gencap_cost-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap_cost-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'energy_model-gencap_cost-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap_cost-scenario-group-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap_cost-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap_cost-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-gencap_cost-year-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-gencap_cost-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'energy_model-gencap_cost-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'energy_model-gencap_cost-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'energy_model-gencap_cost-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-gencap_cost-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'gencap_cost'
        }, 'figure'),
        State({
            'type': 'energy_model-gencap_cost-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-gencap_cost-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-gencap_cost-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-gencap_cost-scenario-group-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'energy_model-gencap_cost-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'energy_model-gencap_cost-text-switch',
                'index': ALL
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _aggregates, _scenarios, _scenario_group, _scenario, _regions, _years, _pattern, _text,
                         _download,_r_style, _y_style, _canvas, _data, _s_style, _m_style, _g_style, _pattern_style, _text_style):
        #print('updating gencap_cost plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-gencap_cost-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-gencap_cost-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Capicity Cost Cost'].to_csv, "gencap_cost.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _g_style, _pattern_style, _text_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-gencap_cost-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}

            df = data_handler.processed_data['Power System Models']['Capicity Cost Cost']
            unique_scenarios = df['scenario'].unique().tolist()
            scens = _scenarios[idx]
            if _scenario_group[idx] != 'ALL':
                scenarios = [scenario for scenario in unique_scenarios if
                             scenario.split('|')[1] == _scenario_group[idx]]
                scens += scenarios

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', df,
                                           _aggregates[idx],
                                           scens,
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _g_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['Power System Models']['Capicity Cost Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _g_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'} 
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['Power System Models']['Capicity Cost Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}

            df = data_handler.processed_data['Power System Models']['Capicity Cost Cost']
            unique_scenarios = df['scenario'].unique().tolist()
            scens = _scenarios[idx]
            if _scenario_group[idx] != 'ALL':
                scenarios = [scenario for scenario in unique_scenarios if scenario.split('|')[1] == _scenario_group[idx]]
                scens += scenarios

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', df,
                                           _aggregates[idx],
                                           scens,
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data], _s_style, _m_style, _g_style, _pattern_style, _text_style
