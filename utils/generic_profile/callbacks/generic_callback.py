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
        Output(
            {
                'type': 'generic-scenario-group-select',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'generic-report-type-select',
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
            'type': 'generic-report-type-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        # Detail level select (per-window). Value is integer number of segments to keep.
        Input({
            'type': 'generic-detail-level-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'generic-scenario-group-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
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
                'type': 'generic-byFuel-switch',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'checked'
        ),
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
            'type': 'generic-compare-scenario-select',
            'index': ALL,
            'model': MATCH,
            'name': MATCH
        }, 'value'),
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
        State(
            {
                'type': 'generic-scenario-group-select',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'generic-report-type-select',
                'index': ALL,
                'model': MATCH,
                'name': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _report_type, _detail_levels, _group_scen, _scenarios, _scenario, _regions, _years, _units, _byFuel, _pattern, _text,
                           _compare_scenario, _download, _r_style, _y_style, _canvas, _data, _s_style, _m_style, _u_style, _pattern_style,
                           _text_style, _group_style, _report_style):
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = trigger_id['model']
        name = trigger_id['name']
        # print(f'updating {name}, {model} plot')

        if 'generic-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'generic-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _u_style, _pattern_style, _text_style, _group_style, _report_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'generic-plot-select')):
                idx = i
                break

        # print('idx:', idx, 'plot type:', _p_type[idx])
        profile = data_handler.profiles[model]
        patterns = [profile.pattern_from_key(key) for key in _scenarios[idx]]
        # print('patterns:', patterns)

        # helper to reduce/detail-aggregate while preserving 'fuel' if present
        def _group_reduce(df_to_reduce):
            """
            Group-reduce numeric columns while preserving non-numeric grouping keys.
            Includes 'fuel' in the group keys when the column exists to avoid dropping it.
            """
            # base grouping order matches previous behaviour
            group_cols = ["variable", "region", "time", 'scenario', 'unit']
            if 'fuel' in df_to_reduce.columns:
                # insert fuel after region for readability (order doesn't change semantics)
                group_cols = ["variable", "region", "fuel", "time", 'scenario', 'unit']
            return df_to_reduce.groupby(group_cols).sum(numeric_only=True).reset_index()

        def _apply_compare_scenario(df, compare_val, model):
            """
            Apply scenario comparison logic with proper handling of missing values.
            Uses outer merge and fillna(0) to handle cases where values exist in one scenario but not the other.
            This implements the bug fix from generation_capacity.py.
            """
            if model == 'Generic Comparison':
                df['model'] = df['scenario'].apply(lambda x: x.split('|')[0])
                to_compare = df[df['base_scenario'] == compare_val].copy()

                # Build merge columns - include fuel if present
                merge_cols = ['region', 'time', 'variable', 'unit', 'model']
                if 'fuel' in df.columns:
                    merge_cols.append('fuel')

                # Use outer merge to preserve rows that exist in either scenario
                df = df.merge(to_compare, on=merge_cols, suffixes=('', '_compare'), how='outer')

                # Drop duplicate scenario columns
                drop_cols = [c for c in ['base_scenario_compare', 'scenario_compare'] if c in df.columns]
                if drop_cols:
                    df = df.drop(columns=drop_cols)
            else:
                to_compare = df[df['scenario'] == compare_val].copy()

                # Build merge columns - include fuel if present
                merge_cols = ['region', 'time', 'variable', 'unit']
                if 'fuel' in df.columns:
                    merge_cols.append('fuel')

                # Use outer merge to preserve rows that exist in either scenario
                df = df.merge(to_compare, on=merge_cols, suffixes=('', '_compare'), how='outer')

                if 'scenario_compare' in df.columns:
                    df = df.drop(columns=['scenario_compare'])

            # Handle missing values: fillna(0) for both value columns before subtraction
            if 'value_compare' in df.columns:
                df['value'] = df['value'].fillna(0)
                df['value_compare'] = df['value_compare'].fillna(0)
                df['value'] = df['value'] - df['value_compare']

            # Clean up comparison columns
            df = df[[col for col in df.columns if not col.endswith('_compare')]]
            return df

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            _report_style[idx] = {'display': 'block'}
            if _group_style is not None and len(_group_scen) > 0:
                _group_style[idx] = {'display': 'block'}

            df = data_handler.processed_data[model][name].copy()
            if _group_scen is not None:
                if len(_group_scen) > 0:
                    _scenarios[idx] += df[df['base_scenario'] == _group_scen[idx]]['scenario'].unique().tolist()
                    _scenarios[idx] = list(set(_scenarios[idx]))

            # Apply compare-to-scenario if selected
            if _compare_scenario is not None and len(_compare_scenario) > idx and _compare_scenario[idx] is not None and _compare_scenario[idx] != 'None':
                df = _apply_compare_scenario(df, _compare_scenario[idx], model)

            # Preprocess dataframe according to selected detail level (truncate variable by '|' segments)
            df_work = df.copy()
            try:
                level = int(_detail_levels[idx]) if (_detail_levels is not None and len(_detail_levels) > idx and _detail_levels[idx] is not None) else None
            except Exception:
                level = None
            if level is not None:
                # truncate variable to first `level` segments separated by '|'
                def truncate_var(v):
                    s = str(v) if v is not None else ''
                    parts = s.split('|')
                    if len(parts) <= level:
                        return s
                    return '|'.join(parts[:level])

                df_work['variable'] = df_work['variable'].astype(str).apply(truncate_var)
                df_work = _group_reduce(df_work)
                 # mark that this df is detail-reduced so plot helpers can skip remapping
                df_work['_detail_reduced'] = True

            # Always render using the (possibly reduced) dataframe; aggregation is disabled
            _canvas[idx] = render_plot('By Year',
                                       name,
                                       df_work,
                                       False,
                                       _scenarios[idx],
                                       _regions[idx],
                                       _units[idx],
                                       _years[idx], scenario=_scenario[idx],
                                       pattern_active=_pattern[idx], text_active=_text[idx], pattern_list=patterns,
                                       report_type=_report_type[idx], use_fuel=_byFuel[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _report_style[idx] = {'display': 'block'}
            if _group_style is not None and len(_group_scen) > 0:
                _group_style[idx] = {'display': 'none'}
            # Prepare df_work for trend
            df = data_handler.processed_data[model][name].copy()
            # Apply compare-to-scenario if selected
            if _compare_scenario is not None and len(_compare_scenario) > idx and _compare_scenario[idx] is not None and _compare_scenario[idx] != 'None':
                df = _apply_compare_scenario(df, _compare_scenario[idx], model)

            df_work = df.copy()
            try:
                level = int(_detail_levels[idx]) if (_detail_levels is not None and len(_detail_levels) > idx and _detail_levels[idx] is not None) else None
            except Exception:
                level = None
            if level is not None:
                df_work['variable'] = df_work['variable'].astype(str).apply(lambda v: '|'.join(str(v).split('|')[:level]) if v is not None else '')
                df_work = _group_reduce(df_work)
                df_work['_detail_reduced'] = True

            _canvas[idx] = render_plot('Trend Over Years',
                                       name,
                                       df_work,
                                       False,
                                       _scenarios[idx],
                                       _regions[idx],
                                       _units[idx],
                                       _years[idx], scenario=_scenario[idx], pattern_list=patterns,
                                       report_type=_report_type[idx], use_fuel=_byFuel[idx])
        elif _p_type[idx] == 'Trend in one Year':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _report_style[idx] = {'display': 'none'}
            if _group_style is not None and len(_group_scen) > 0:
                _group_style[idx] = {'display': 'none'}
            df = data_handler.processed_data[model][name].copy()
            # Apply compare-to-scenario if selected
            if _compare_scenario is not None and len(_compare_scenario) > idx and _compare_scenario[idx] is not None and _compare_scenario[idx] != 'None':
                df = _apply_compare_scenario(df, _compare_scenario[idx], model)

            df_work = df.copy()
            try:
                level = int(_detail_levels[idx]) if (_detail_levels is not None and len(_detail_levels) > idx and _detail_levels[idx] is not None) else None
            except Exception:
                level = None
            if level is not None:
                df_work['variable'] = df_work['variable'].astype(str).apply(lambda v: '|'.join(str(v).split('|')[:level]) if v is not None else '')
                df_work = _group_reduce(df_work)
                df_work['_detail_reduced'] = True

            _canvas[idx] = render_plot('Trend in one Year',
                                       name,
                                       df_work,
                                       False,
                                       _scenarios[idx],
                                       _regions[idx],
                                       _units[idx],
                                       _years[idx], scenario=_scenario[idx], pattern_list=patterns, use_fuel=_byFuel[idx])
        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _report_style[idx] = {'display': 'none'}
            if _group_style is not None and len(_group_scen) > 0:
                _group_style[idx] = {'display': 'none'}
            df = data_handler.processed_data[model][name].copy()
            # Apply compare-to-scenario if selected
            if _compare_scenario is not None and len(_compare_scenario) > idx and _compare_scenario[idx] is not None and _compare_scenario[idx] != 'None':
                df = _apply_compare_scenario(df, _compare_scenario[idx], model)

            df_work = df.copy()
            try:
                level = int(_detail_levels[idx]) if (_detail_levels is not None and len(_detail_levels) > idx and _detail_levels[idx] is not None) else None
            except Exception:
                level = None
            if level is not None:
                df_work['variable'] = df_work['variable'].astype(str).apply(lambda v: '|'.join(str(v).split('|')[:level]) if v is not None else '')
                df_work = _group_reduce(df_work)
                df_work['_detail_reduced'] = True

            _canvas[idx] = render_plot('Pie Chart',
                                       name,
                                       df_work,
                                       False,
                                       _scenarios[idx],
                                       _regions[idx],
                                       _units[idx],
                                       _years[idx], scenario=_scenario[idx], pattern_list=patterns, use_fuel=_byFuel[idx])
        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _u_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            _report_style[idx] = {'display': 'block'}
            if _group_style is not None and len(_group_scen) > 0:
                _group_style[idx] = {'display': 'block'}

            df = data_handler.processed_data[model][name].copy()
            if _group_scen is not None:
                if len(_group_scen) > 0:
                    _scenarios[idx] += df[df['base_scenario'] == _group_scen[idx]]['scenario'].unique().tolist()
                    _scenarios[idx] = list(set(_scenarios[idx]))
            # Apply compare-to-scenario if selected
            if _compare_scenario is not None and len(_compare_scenario) > idx and _compare_scenario[idx] is not None and _compare_scenario[idx] != 'None':
                df = _apply_compare_scenario(df, _compare_scenario[idx], model)

            df_work = df.copy()
            try:
                level = int(_detail_levels[idx]) if (_detail_levels is not None and len(_detail_levels) > idx and _detail_levels[idx] is not None) else None
            except Exception:
                level = None
            if level is not None:
                df_work['variable'] = df_work['variable'].astype(str).apply(lambda v: '|'.join(str(v).split('|')[:level]) if v is not None else '')
                df_work = _group_reduce(df_work)
                df_work['_detail_reduced'] = True

            _canvas[idx] = render_plot('By Region',
                                       name,
                                       df_work,
                                       False,
                                       _scenarios[idx],
                                       _regions[idx],
                                       _units[idx],
                                       _years[idx], scenario=_scenario[idx],
                                       pattern_active=_pattern[idx], text_active=_text[idx], pattern_list=patterns,
                                       report_type=_report_type[idx], use_fuel=_byFuel[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in
                                             _data], _s_style, _m_style, _u_style, _pattern_style, _text_style, _group_style, _report_style
