import dash
import pandas as pd
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.overview import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Overview'
        }, 'figure'),

        Output({
            'type': 'energy_model-overview-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-overview-fill-switch',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-overview-version-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-overview-version-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'energy_model-overview-version-select',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-overview-plot-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-overview-relative',
                'index': ALL,
            }, 'checked'
        ),
        Input(
            {
                'type': 'energy_model-overview-compare-reference',
                'index': ALL,
            }, 'checked'
        ),
        Input({
            'type': 'energy_model-overview-groupby-toggle',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'energy_model-overview-fill-switch',
                'index': ALL,
            }, 'checked'
        ),
        Input({
            'type': 'energy_model-overview-scenario-group-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-overview-version-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'energy_model-overview-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Overview'
        }, 'figure'),

        State({
            'type': 'energy_model-overview-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'energy_model-overview-fill-switch',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-overview-version-select',
            'index': ALL
        }, 'style'),

        prevent_initial_call=True
    )
    def update_overview(_p_type, _relative, _compare2ref, _groupby, _fill, _scenarios, _version_values, _fill_checked, _canvas, _data, _fillswitch, _v_style):
        #print('updating overview plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-overview-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-overview-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Overview'].to_csv,
                                             "overview.csv")
            return _canvas, _data, _fillswitch, _v_style, [dash.no_update for _ in _v_style], [dash.no_update for _ in _v_style]

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-overview-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])
        _groupby_model = _groupby[idx] == 1
        _groupby_scenario = _groupby[idx] == 2
        _groupby_version = _groupby[idx] == 3

        # prepare version-select outputs and populate when scenario-group changes
        v_style = list(_v_style)
        v_values = _version_values
        v_data = [dash.no_update for _ in v_style]
        if trigger_id['type'] == 'energy_model-overview-scenario-group-select':
            # find which index triggered
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-overview-scenario-group-select')):
                    idx = i
                    break

            df_all = data_handler.processed_data['Power System Models']['Overview']
            unique_scenarios = df_all['scenario'].unique().tolist()
            group = _scenarios[idx]
            # collect versions for the selected group; if group == 'ALL' collect all versions
            if group == 'ALL':
                versions = sorted({s.split('|')[2] for s in unique_scenarios if len(s.split('|')) > 2})
            else:
                versions = sorted({s.split('|')[2] for s in unique_scenarios if len(s.split('|')) > 2 and s.split('|')[1] == group})

            if versions:
                v_style[idx] = {'display': 'block'}
                v_values[idx] = []
                v_data[idx] = [{'label': v, 'value': v} for v in versions]
            else:
                v_style[idx] = {'display': 'none'}
                v_values[idx] = None
                v_data[idx] = []

        df = data_handler.processed_data['Power System Models']['Overview']

        df = df[df.variable == _p_type[idx]].copy()

        if _compare2ref[idx]:
            df[['model', 'base_scenario', 'version']] = df['scenario'].apply(lambda x: pd.Series(
                [x.split('|')[0], '|'.join(x.split('|')[1:-1]) if len(x.split('|')) > 2 else x.split('|')[1],
                 x.split('|')[-1] if len(x.split('|')) > 2 else '']))
            reference_data = df[df['base_scenario'].str.contains('Reference')]
            if reference_data.empty:
                print("No Reference scenario found for comparison.")
            else:
                merged = df.merge(reference_data, on=['model', 'version', 'time', 'variable', 'region'],
                                  suffixes=('', '_ref'), how='outer')
                merged['value_ref'] = merged['value_ref'].fillna(0)
                merged['value'] = merged['value'] - merged['value_ref']
                df = merged[['scenario', 'time', 'variable', 'region', 'value']]

        # filter by scenario group if not ALL
        if _scenarios[idx] != 'ALL':
            df = df[df['scenario'].str.contains(_scenarios[idx])]
        # additionally filter by selected versions (works also when scenario group == 'ALL')
        if v_values and v_values[idx]:
            sel = set(v_values[idx])
            df = df[[len(s.split('|')) > 2 and s.split('|')[2] in sel for s in df['scenario']]]

        _canvas[idx] = render_plot(_p_type[idx], df,
                                   _groupby_model, _groupby_scenario, _groupby_version, _fill[idx], _relative[idx])

        _fillswitch[idx] = {'display': 'none'}
        if _groupby[idx] > 0:
            _fillswitch[idx] = {'display': 'block'}

        return _canvas, [dash.no_update for _ in _data], _fillswitch, v_style, v_values, v_data
