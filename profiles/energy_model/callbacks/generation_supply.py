import dash
import pandas as pd
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.generation_supply import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Supply'
        }, 'figure'),
        Output({
            'type': 'energy_model-supply-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-supply-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-supply-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-supply-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-supply-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-supply-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-supply-version-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-supply-version-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'energy_model-supply-version-select',
            'index': ALL
        }, 'data'),
        Output(
            {
                'type': 'energy_model-supply-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'energy_model-supply-text-switch',
                'index': ALL
            },
            'style'
        ),
        Output({
            'type': 'energy_model-supply-report-type-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'energy_model-supply-plot-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-supply-compare-reference',
                'index': ALL,
            }, 'checked'
        ),
        Input({
            'type': 'energy_model-supply-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'energy_model-supply-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-supply-scenario-group-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-supply-version-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-supply-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-supply-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-supply-report-type-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-supply-year-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-supply-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'energy_model-supply-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'energy_model-supply-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'energy_model-supply-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-supply-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Supply'
        }, 'figure'),
        State({
            'type': 'energy_model-supply-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-supply-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-supply-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-supply-scenario-group-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-supply-version-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'energy_model-supply-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'energy_model-supply-text-switch',
                'index': ALL
            },
            'style'
        ),
        State({
            'type': 'energy_model-supply-report-type-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_supply(_p_type, _compare2ref, _aggregates, _scenarios, _scenario_group, _scenario_version, _scenario, _regions, _report_type, _years, _pattern, _text,
                         _download,_r_style, _y_style, _canvas, _data, _s_style, _m_style, _g_style, _v_style, _pattern_style, _text_style, _report_type_style):
        #print('updating supply plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        v_style = list(_v_style)
        v_values = _scenario_version
        v_data = [dash.no_update for _ in v_style]

        if 'energy_model-supply-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-supply-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Supply'].to_csv, "supply.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _g_style, [dash.no_update for _ in v_style], [dash.no_update for _ in v_style], [dash.no_update for _ in v_style], [dash.no_update for _ in v_style], [dash.no_update for _ in v_style], [dash.no_update for _ in v_style]

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-supply-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])
        df = data_handler.processed_data['Power System Models']['Supply']
        unique_scenarios = df['scenario'].unique().tolist()

        scens = list(_scenarios[idx]) if _scenarios and _scenarios[idx] is not None else []
        # handle scenario_group being a list (MultiSelect)
        selected_groups = _scenario_group[idx] if isinstance(_scenario_group, list) or hasattr(_scenario_group, '__len__') else [_scenario_group]
        if selected_groups and len(selected_groups) > 0 and not (len(selected_groups) == 1 and selected_groups[0] == ''):
            # if 'ALL' is selected include all unique scenarios
            if 'ALL' in selected_groups:
                scenarios = unique_scenarios
            else:
                scenarios = [scenario for scenario in unique_scenarios if scenario.split('|')[1] in selected_groups]

            # if scenario_group changed update scenario_version style, data and value
            if trigger_id['type'] == 'energy_model-supply-scenario-group-select':
                # find which index triggered
                idx = 0
                for i, id in enumerate(ctx.inputs_list[0]):
                    if ((id['id']['index'] == trigger_id['index']) and (id['id']['type'] == 'energy_model-supply-scenario-group-select')):
                        idx = i
                        break

                # collect versions for the selected groups
                groups = _scenario_group[idx] if _scenario_group[idx] is not None else []
                versions = []
                if groups:
                    if 'ALL' in groups:
                        versions = sorted({s.split('|')[2] for s in unique_scenarios if len(s.split('|')) > 2})
                    else:
                        versions = sorted({s.split('|')[2] for s in unique_scenarios if len(s.split('|')) > 2 and s.split('|')[1] in groups})

                if versions:
                    v_style[idx] = {'display': 'block'}
                    v_values[idx] = []
                    v_data[idx] = [{'label': v, 'value': v} for v in versions]
                else:
                    v_style[idx] = {'display': 'none'}
                    v_values[idx] = []
                    v_data[idx] = []

            if v_values and v_values[idx]:
                # filter scenarios by version
                scenarios = [scenario for scenario in scenarios if scenario.split('|')[2] in v_values[idx]]

            scens = list(set(scens + scenarios))

        if _compare2ref[idx]:
            df[['model', 'base_scenario', 'version']] = df['scenario'].apply(lambda x: pd.Series(
                [x.split('|')[0], '|'.join(x.split('|')[1:-1]) if len(x.split('|')) > 2 else x.split('|')[1],
                 x.split('|')[-1] if len(x.split('|')) > 2 else '']))

            reference_data = df[df['base_scenario'].str.contains('Reference')].copy()

            if reference_data.empty:
                print("No Reference scenario found for comparison.")
            else:
                results = []

                for scenario in df['scenario'].unique():
                    scenario_df = df[df['scenario'] == scenario].copy()

                    # Get model and version for this scenario
                    model = scenario_df['model'].iloc[0]
                    version = scenario_df['version'].iloc[0]

                    # Filter reference data to matching model/version
                    ref_subset = reference_data[(reference_data['model'] == model) &
                                                (reference_data['version'] == version)]

                    merged = scenario_df.merge(ref_subset,
                                               on=['model', 'version', 'time', 'variable', 'region'],
                                               suffixes=('', '_ref'),
                                               how='outer')

                    merged['value_ref'] = merged['value_ref'].fillna(0)
                    merged['value'] = merged['value'].fillna(0)
                    merged['value'] = merged['value'] - merged['value_ref']

                    # Preserve scenario for reference-only rows
                    merged['scenario'] = scenario

                    results.append(merged[['scenario', 'time', 'variable', 'region', 'value']])

                df = pd.concat(results, ignore_index=True)

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            _report_type_style[idx] = {'display': 'block'}



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
            v_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['Power System Models']['Supply'],
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
            v_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['Power System Models']['Supply'],
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



            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', df,
                                           _aggregates[idx],
                                           scens,
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx], report_type=_report_type[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data], _s_style, _m_style, _g_style, v_style, v_values, v_data, _pattern_style, _text_style, _report_type_style
