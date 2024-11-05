import dash
from dash import Output, Input, State, ALL

from profiles.energy_model.visualization_scripts.transmission_capacity import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'transmission_capacity'
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
            'type': 'energy_model-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissioncapacity-year-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'transmission_capacity'
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
        prevent_initial_call=True
    )
    def update_transmissioncapacity(_p_type, _scenarios, _scenario_group, _scenario, _years, _canvas, _s_style, _m_style, _g_style):
        #print('updating transmissioncapacity plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if (id['id']['index'] == trigger_id['index']):
                idx = i
                break

        if _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _g_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Map Plot',
                                       data_handler.processed_data['Power System Models']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx]
                                       )
        elif _p_type[idx] == 'Bar Plot':
            df = data_handler.processed_data['Power System Models']['Transmission Capacity']
            unique_scenarios = df['scenario'].unique().tolist()
            scens = _scenarios[idx]
            if _scenario_group[idx] != 'ALL':
                scenarios = [scenario for scenario in unique_scenarios if
                             scenario.split('|')[1] == _scenario_group[idx]]
                scens += scenarios
                
            _g_style[idx] = {'display': 'block'}
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Bar Plot',
                                       data_handler.processed_data['Power System Models']['Transmission Capacity'],
                                       scens,
                                       _years[idx]
                                       )

        return _canvas, _s_style, _m_style, _g_style
