import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.transmission_capacity import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Transmission Capacity'
        }, 'figure'),
        Output({
            'type': 'energy_model-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissioncapacity-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissioncapacity-version-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissioncapacity-version-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'energy_model-transmissioncapacity-version-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'energy_model-transmissioncapacity-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissioncapacity-lines-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissioncapacity-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-transmissioncapacity-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-scenario-group-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-version-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-lines-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Transmission Capacity'
        }, 'figure'),
        State({
            'type': 'energy_model-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissioncapacity-scenario-group-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissioncapacity-version-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissioncapacity-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissioncapacity-lines-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissioncapacity-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_transmissioncapacity(_p_type, _scenarios, _scenario_group, _scenario_version, _scenario, _years, _lines, _d_button, _canvas,
                                    _s_style, _m_style, _g_style, _y_style, _l_style, _data, _g_v_style):
        # print('updating transmissioncapacity plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        v_style = list(_g_v_style)
        v_values = _scenario_version
        v_data = [dash.no_update for _ in v_style]
        if 'energy_model-transmissioncapacity-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-transmissioncapacity-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Transmission Capacity'].to_csv, "transmissioncapacity.csv")
            return _canvas, _s_style, _m_style, _g_style,  v_style, v_values, v_data, _y_style, _l_style, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if (id['id']['index'] == trigger_id['index']):
                idx = i
                break


        df = data_handler.processed_data['Power System Models']['Transmission Capacity']
        unique_scenarios = df['scenario'].unique().tolist()

        v_style = list(_g_v_style)
        v_values = _scenario_version
        v_data = [dash.no_update for _ in v_style]
        scens = _scenarios[idx]
        if _scenario_group[idx] != '':
            if _scenario_group[idx] == 'ALL':
                scenarios = unique_scenarios
            else:
                scenarios = [scenario for scenario in unique_scenarios if
                             scenario.split('|')[1] == _scenario_group[idx]]

            # if _scenario_group changed update scenario_version style, data and value
            scenario_group_changed = False

            if trigger_id['type'] == 'energy_model-transmissioncapacity-scenario-group-select':
                scenario_group_changed = True
                # find which index triggered
                idx = 0
                for i, id in enumerate(ctx.inputs_list[0]):
                    if ((id['id']['index'] == trigger_id['index']) and
                            (id['id']['type'] == 'energy_model-transmissioncapacity-scenario-group-select')):
                        idx = i
                        break

                # collect versions for the selected group
                group = _scenario_group[idx]
                versions = []
                if group != '':
                    if group == 'ALL':
                        versions = sorted({s.split('|')[2] for s in unique_scenarios if
                                           len(s.split('|')) > 2})
                    else:
                        versions = sorted({s.split('|')[2] for s in unique_scenarios if
                                           len(s.split('|')) > 2 and s.split('|')[1] == group})

                if versions:
                    v_style[idx] = {'display': 'block'}
                    v_values[idx] = []
                    v_data[idx] = [{'label': v, 'value': v} for v in versions]
                else:
                    v_style[idx] = {'display': 'none'}
                    v_values[idx] = []
                    v_data[idx] = []

            if len(v_values[idx]) > 0:
                # filter scenarios by version
                scenarios = [scenario for scenario in scenarios if
                             scenario.split('|')[2] in v_values[idx]]
            scens += scenarios

        if _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _l_style[idx] = {'display': 'none'}
            v_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Map Plot',
                                       data_handler.processed_data['Power System Models']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Per Line Bar Plot':
            _g_style[idx] = {'display': 'block'}
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _l_style[idx] = {'display': 'none'}
            v_style[idx] = {'display': 'block'}
            v_data[idx] = v_data[idx]
            _canvas[idx] = render_plot('Per Line Bar Plot',
                                       data_handler.processed_data['Power System Models']['Transmission Capacity'],
                                       scens,
                                       _years[idx],
                                        _lines[idx]
                                       )
        elif _p_type[idx] == 'Per Year Bar Plot':

            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _g_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _l_style[idx] = {'display': 'block'}
            v_style[idx] = {'display': 'block'}
            v_data[idx] = v_data[idx]
            _canvas[idx] = render_plot('Per Year Bar Plot',
                                       data_handler.processed_data['Power System Models']['Transmission Capacity'],
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
            v_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Trends Over Years',
                                       data_handler.processed_data['Power System Models']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx],
                                        _lines[idx]
                                       )

        return _canvas, _s_style, _m_style, _g_style,  v_style, v_values, v_data,_y_style, _l_style, [dash.no_update for _ in _data]
