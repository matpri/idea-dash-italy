import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.transmission_flow import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'transmission_flow'
        }, 'figure'),
        Output({
            'type': 'energy_model-transmissionflow-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissionflow-scenario-group-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'energy_model-transmissionflow-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-transmissionflow-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissionflow-scenario-group-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'energy_model-transmissionflow-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissionflow-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-transmissionflow-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'transmission_flow'
        }, 'figure'),
        State({
            'type': 'energy_model-transmissionflow-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissionflow-scenario-group-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'energy_model-transmissionflow-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_transmissionflow(_p_type, _scenarios, _scenario_group, _scenario, _years, _d_button, _canvas,
                                    _s_style, _m_style, _g_style, _data):
        # print('updating transmissionflow plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        if 'energy_model-transmissionflow-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-transmissionflow-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Transmission Flow'].to_csv, "transmissionflow.csv")
            return _canvas, _s_style, _m_style, _g_style, _data

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
                                       data_handler.processed_data['Power System Models']['Transmission Flow'],
                                       _scenario[idx],
                                       _years[idx]
                                       )
        elif _p_type[idx] == 'Bar Plot':
            df = data_handler.processed_data['Power System Models']['Transmission Flow']
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
                                       data_handler.processed_data['Power System Models']['Transmission Flow'],
                                       scens,
                                       _years[idx]
                                       )

        return _canvas, _s_style, _m_style, _g_style, _data
