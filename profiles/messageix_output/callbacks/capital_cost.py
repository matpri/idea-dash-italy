import dash
from dash import Output, Input, State, ALL, dcc

from profiles.messageix_output import utils
from profiles.messageix_output.visualization_scripts.capital_cost import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'messageix_output',
            'viz': 'capital_cost'
        }, 'figure'),
        Output({
            'type': 'messageix-capital_cost-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-capital_cost-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-capital_cost-variable-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-capital_cost-variable-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'messageix-capital_cost-variable-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'messageix-capital_cost-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'messageix-capital_cost-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-capital_cost-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output(
            {
                'type': 'messageix-capital_cost-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'messageix-capital_cost-text-switch',
                'index': ALL
            },
            'style'
        ),
        Input({
            'type': 'messageix-capital_cost-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-capital_cost-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'messageix-capital_cost-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-capital_cost-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-capital_cost-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-capital_cost-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-capital_cost-variable-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'messageix-capital_cost-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'messageix-capital_cost-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'messageix-capital_cost-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'messageix-capital_cost-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-capital_cost-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-capital_cost-variable-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-capital_cost-variable-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'messageix_output',
            'viz': 'capital_cost'
        }, 'figure'),
        State({
            'type': 'messageix-capital_cost-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'messageix-capital_cost-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-capital_cost-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'messageix-capital_cost-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'messageix-capital_cost-text-switch',
                'index': ALL
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_capital_cost(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _variables, _pattern, _text,
                         _download,_r_style, _y_style, _v_style, _v_data, _canvas, _data, _s_style, _m_style, _pattern_style, _text_style):
        print('updating capital_cost plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'messageix-capital_cost-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'messageix-capital_cost-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'].to_csv, "capital_cost.csv")
            return _canvas, _r_style, _y_style, _v_style, _v_data, _variables, _data, _s_style, _m_style, _pattern_style, _text_style
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'messageix-capital_cost-plot-select')):
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
            _v_style[idx] = {'display': 'none'}

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx], variable=_variables[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _v_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], variable=_variables[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _v_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], variable=_variables[idx])

        elif _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'none'}
            _v_style[idx] = {'display': 'block'}

            if 'messageix-capital_cost-aggregate-switch' in trigger_id['type']:
                if _aggregates[idx] is not None:
                    df_scen = data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'].copy(deep=True)
                    if _aggregates[idx]:
                        df_scen['variable'] = df_scen["variable"].map(utils.groups).fillna(df_scen["variable"])
                    else:
                        df_scen['variable'] = df_scen["variable"].map(utils.names).fillna(df_scen["variable"])
                    df_scen = df_scen[(df_scen['region'] == _regions[idx]) & (df_scen['time'] == _years[idx]) & (df_scen['scenario'] == _scenario[idx])]

                    _v_data[idx] = [{'label': 'All', 'value': 'All'}] + [{'label': var, 'value': var} for var in df_scen.variable.unique().tolist()]
                    _variables[idx] = 'All'


            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Map Plot', data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], variable=_variables[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            _v_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['MESSAGEix-Canada']['Capital Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx], variable=_variables[idx])

        return _canvas, _r_style, _y_style, _v_style, _v_data, _variables, [dash.no_update for _ in _data], _s_style, _m_style, _pattern_style, _text_style
