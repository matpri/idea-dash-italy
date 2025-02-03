import dash
from dash import Output, Input, State, ALL, dcc

from profiles.messageix_output import utils
from profiles.messageix_output.visualization_scripts.final_energy import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'messageix_output',
            'viz': 'final_energy'
        }, 'figure'),
        Output({
            'type': 'messageix-final_energy-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-final_energy-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-final_energy-variable-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-final_energy-variable-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'messageix-final_energy-variable-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'messageix-final_energy-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'messageix-final_energy-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-final_energy-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output(
            {
                'type': 'messageix-final_energy-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'messageix-final_energy-text-switch',
                'index': ALL
            },
            'style'
        ),
        Input({
            'type': 'messageix-final_energy-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-final_energy-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'messageix-final_energy-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-final_energy-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-final_energy-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-final_energy-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-final_energy-variable-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'messageix-final_energy-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'messageix-final_energy-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'messageix-final_energy-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'messageix-final_energy-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-final_energy-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-final_energy-variable-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-final_energy-variable-select',
            'index': ALL
        }, 'data'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'messageix_output',
            'viz': 'final_energy'
        }, 'figure'),
        State({
            'type': 'messageix-final_energy-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'messageix-final_energy-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-final_energy-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'messageix-final_energy-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'messageix-final_energy-text-switch',
                'index': ALL
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_final_energy(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _variables, _pattern, _text,
                         _download,_r_style, _y_style, _v_style, _v_data, _canvas, _data, _s_style, _m_style, _pattern_style, _text_style):
        print('updating final_energy plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'messageix-final_energy-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'messageix-final_energy-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['MESSAGEix-Canada']['Final Energy'].to_csv, "final_energy.csv")
            return _canvas, _r_style, _y_style, _v_style, _v_data, _variables, _data, _s_style, _m_style, _pattern_style, _text_style
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'messageix-final_energy-plot-select')):
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
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['MESSAGEix-Canada']['Final Energy'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx], variables=_variables[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['MESSAGEix-Canada']['Final Energy'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], variables=_variables[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['MESSAGEix-Canada']['Final Energy'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], variables=_variables[idx])

        elif _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'none'}
            _v_style[idx] = {'display': 'block'}

            if 'messageix-final_energy-aggregate-switch' in trigger_id['type']:
                if _aggregates[idx] is not None:
                    df_scen = data_handler.processed_data['MESSAGEix-Canada']['Final Energy'].copy(deep=True)
                    if _aggregates[idx]:
                        df_scen['variable'] = df_scen["variable"].map(utils.groups).fillna(df_scen["variable"])
                    else:
                        df_scen['variable'] = df_scen["variable"].map(utils.names).fillna(df_scen["variable"])
                    df_scen = df_scen[(df_scen['region'] == _regions[idx]) & (df_scen['time'] == _years[idx]) & (df_scen['scenario'] == _scenario[idx])]

                    _v_data[idx] = [{'label': var, 'value': var} for var in df_scen.variable.unique().tolist()]
                    _variables[idx] = _v_data[idx]


            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Map Plot', data_handler.processed_data['MESSAGEix-Canada']['Final Energy'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx], variables=_variables[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['MESSAGEix-Canada']['Final Energy'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx], variables=_variables[idx])

        return _canvas, _r_style, _y_style, _v_style, _v_data, _variables, [dash.no_update for _ in _data], _s_style, _m_style, _pattern_style, _text_style
