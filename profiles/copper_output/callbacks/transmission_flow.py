import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.transmission_flow import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'copper',
            'viz': 'transmission_flow'
        }, 'figure'),
        Output({
            'type': 'copper-transmissionflow-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-transmissionflow-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-transmissionflow-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-transmissionflow-lines-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-transmissionflow-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'copper-transmissionflow-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-transmissionflow-scenario-group-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper-transmissionflow-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-transmissionflow-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-transmissionflow-lines-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-transmissionflow-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'copper',
            'viz': 'transmission_flow'
        }, 'figure'),
        State({
            'type': 'copper-transmissionflow-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-transmissionflow-scenario-group-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-transmissionflow-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-transmissionflow-lines-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-transmissionflow-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_transmissionflow(_p_type, _scenarios, _scenario_group, _scenario, _years, _lines, _d_button, _canvas,
                                    _s_style, _m_style, _g_style, _y_style, _l_style, _data):
        # print('updating transmissionflow plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        if 'copper-transmissionflow-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper-transmissionflow-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER']['Transmission Flow'].to_csv, "transmissionflow.csv")
            return _canvas, _s_style, _m_style, _g_style, _y_style, _l_style, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if (id['id']['index'] == trigger_id['index']):
                idx = i
                break
        if _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _l_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Map Plot',
                                       data_handler.processed_data['COPPER']['Transmission Flow'],
                                       _scenario[idx],
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Per Line Bar Plot':
            df = data_handler.processed_data['COPPER']['Transmission Flow']
            unique_scenarios = df['scenario'].unique().tolist()
            scens = _scenarios[idx]
            if _scenario_group[idx] != 'ALL':
                scenarios = [scenario for scenario in unique_scenarios if
                             scenario.split('|')[1] == _scenario_group[idx]]
                scens += scenarios

            _g_style[idx] = {'display': 'block'}
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _l_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Per Line Bar Plot',
                                       data_handler.processed_data['COPPER']['Transmission Flow'],
                                       scens,
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Per Year Bar Plot':
            df = data_handler.processed_data['COPPER']['Transmission Flow']
            unique_scenarios = df['scenario'].unique().tolist()
            scens = _scenarios[idx]
            if _scenario_group[idx] != 'ALL':
                scenarios = [scenario for scenario in unique_scenarios if
                             scenario.split('|')[1] == _scenario_group[idx]]
                scens += scenarios
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _g_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _l_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('Per Year Bar Plot',
                                       data_handler.processed_data['COPPER']['Transmission Flow'],
                                       scens,
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Trends Over Years':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'none'}
            _l_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Trends Over Years',
                                       data_handler.processed_data['COPPER']['Transmission Flow'],
                                       _scenario[idx],
                                       _years[idx],
                                        _lines[idx]
                                       )

        return _canvas, _s_style, _m_style, _g_style, _y_style, _l_style, _data
