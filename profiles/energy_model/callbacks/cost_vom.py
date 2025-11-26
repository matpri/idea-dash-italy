import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.cost_vom import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'VOM Cost'
        }, 'figure'),
        Output({
            'type': 'energy_model-vom_cost-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-vom_cost-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-vom_cost-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-vom_cost-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-vom_cost-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-vom_cost-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-vom_cost-version-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-vom_cost-version-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'energy_model-vom_cost-version-select',
            'index': ALL
        }, 'data'),
        Output(
            {
                'type': 'energy_model-vom_cost-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'energy_model-vom_cost-text-switch',
                'index': ALL
            },
            'style'
        ),
        Output({
            'type': 'energy_model-vom_cost-report-type-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'energy_model-vom_cost-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'energy_model-vom_cost-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-scenario-group-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-version-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-report-type-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-vom_cost-year-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-vom_cost-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'energy_model-vom_cost-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'energy_model-vom_cost-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'energy_model-vom_cost-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-vom_cost-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'VOM Cost'
        }, 'figure'),
        State({
            'type': 'energy_model-vom_cost-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-vom_cost-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-vom_cost-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-vom_cost-scenario-group-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-vom_cost-version-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'energy_model-vom_cost-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'energy_model-vom_cost-text-switch',
                'index': ALL
            },
            'style'
        ),
        State({
            'type': 'energy_model-vom_cost-report-type-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_vom_cost(_p_type, _aggregates, _scenarios, _scenario_group, _scenario_version, _scenario, _regions, _report_type, _years, _pattern, _text,
                         _download,_r_style, _y_style, _canvas, _data, _s_style, _m_style, _g_style, _v_style, _pattern_style, _text_style, _report_type_style):
        #print('updating vom_cost plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-vom_cost-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-vom_cost-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['VOM Cost'].to_csv, "vom_cost.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _g_style, _v_style, dash.no_update, dash.no_update, _pattern_style, _text_style, _report_type_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-vom_cost-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        # if _scenario_group changed update scenario_version style, data and value
        scenario_group_changed = False

        v_style = list(_v_style)
        v_values = _scenario_version
        v_data = [dash.no_update for _ in v_style]
        if trigger_id['type'] == 'energy_model-vom_cost-scenario-group-select':
            scenario_group_changed = True
            # find which index triggered
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-vom_cost-scenario-group-select')):
                    idx = i
                    break

            df = data_handler.processed_data['Power System Models']['VOM Cost']
            unique_scenarios = df['scenario'].unique().tolist()

            # collect versions for the selected group
            group = _scenario_group[idx]
            versions = []
            if group != 'ALL':
                versions = sorted({s.split('|')[2] for s in unique_scenarios if
                                   len(s.split('|')) > 2 and s.split('|')[1] == group})

            if versions:
                v_style[idx] = {'display': 'block'}
                v_values[idx] = []
                v_data[idx] = [{'label': v, 'value': v} for v in versions]
            else:
                v_style[idx] = {'display': 'none'}
                v_values[idx] = None
                v_data[idx] = []

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            _report_type_style[idx] = {'display': 'block'}

            df = data_handler.processed_data['Power System Models']['VOM Cost']
            unique_scenarios = df['scenario'].unique().tolist()
            scens = _scenarios[idx]
            if _scenario_group[idx] != 'ALL':
                scenarios = [scenario for scenario in unique_scenarios if
                             scenario.split('|')[1] == _scenario_group[idx]]

                if len(v_values[idx]) > 0:
                    # filter scenarios by version
                    scenarios = [scenario for scenario in scenarios if
                                 scenario.split('|')[2] in v_values[idx]]
                scens += scenarios

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', df,
                                           _aggregates[idx],
                                           scens,
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx], report_type=_report_type[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _g_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _report_type_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['Power System Models']['VOM Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], report_type=_report_type[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'} 
            _report_type_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['Power System Models']['VOM Cost'],
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
            _report_type_style[idx] = {'display': 'block'}

            df = data_handler.processed_data['Power System Models']['VOM Cost']
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
                                           pattern_active=_pattern[idx], text_active=_text[idx], report_type=_report_type[idx])


        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data], _s_style, _m_style, _g_style, v_style, v_values, v_data, _pattern_style, _text_style, _report_type_style

