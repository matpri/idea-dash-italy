import dash
from dash import Output, Input, State, ALL, dcc

from profiles.pithos_output.visualization_scripts.transmission_capacity import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'HEC-PITHOS',
            'viz': 'Transmission Capacity'
        }, 'figure'),
        Output({
            'type': 'pithos-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pithos-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pithos-transmissioncapacity-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pithos-transmissioncapacity-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pithos-transmissioncapacity-lines-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pithos-transmissioncapacity-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'pithos-transmissioncapacity-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pithos-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pithos-transmissioncapacity-scenario-group-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'pithos-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pithos-transmissioncapacity-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pithos-transmissioncapacity-lines-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pithos-transmissioncapacity-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'HEC-PITHOS',
            'viz': 'Transmission Capacity'
        }, 'figure'),
        State({
            'type': 'pithos-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pithos-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pithos-transmissioncapacity-scenario-group-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pithos-transmissioncapacity-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pithos-transmissioncapacity-lines-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pithos-transmissioncapacity-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_transmissioncapacity(_p_type, _scenarios, _scenario_group, _scenario, _years, _lines, _d_button, _canvas,
                                    _s_style, _m_style, _g_style, _y_style, _l_style, _data):
        # print('updating transmissioncapacity plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        if 'pithos-transmissioncapacity-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'pithos-transmissioncapacity-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['HEC-PITHOS']['Transmission Capacity'].to_csv, "transmissioncapacity.csv")
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
                                       data_handler.processed_data['HEC-PITHOS']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Per Line Bar Plot':
            df = data_handler.processed_data['HEC-PITHOS']['Transmission Capacity']
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
                                       data_handler.processed_data['HEC-PITHOS']['Transmission Capacity'],
                                       scens,
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Per Year Bar Plot':
            df = data_handler.processed_data['HEC-PITHOS']['Transmission Capacity']
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
                                       data_handler.processed_data['HEC-PITHOS']['Transmission Capacity'],
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
                                       data_handler.processed_data['HEC-PITHOS']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx],
                                        _lines[idx]
                                       )

        return _canvas, _s_style, _m_style, _g_style, _y_style, _l_style, _data
