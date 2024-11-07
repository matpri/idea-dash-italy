import dash
from dash import Output, Input, State, ALL, dcc

from profiles.pypsa_output.visualization_scripts.transmission_flow import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'pypsa_output',
            'viz': 'transmission_flow'
        }, 'figure'),
        Output({
            'type': 'pypsa-transmissionflow-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pypsa-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pypsa-transmissionflow-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'pypsa-transmissionflow-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pypsa-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'pypsa-transmissionflow-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pypsa-transmissionflow-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pypsa-transmissionflow-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'pypsa_output',
            'viz': 'transmission_flow'
        }, 'figure'),
        State({
            'type': 'pypsa-transmissionflow-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pypsa-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pypsa-transmissionflow-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_transmissionflow(_p_type, _scenarios, _scenario, _years, _d_button, _canvas, _s_style, _m_style, _data):
        # print('updating transmissionflow plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'pypsa-transmissionflow-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'pypsa-transmissionflow-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['NRCan-PyPsa']['Transmission Flow'].to_csv,
                                             "transmission_flow.csv")
            return _canvas, _s_style, _m_style, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if (id['id']['index'] == trigger_id['index']):
                idx = i
                break

        if _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('Map Plot',
                                       data_handler.processed_data['NRCan-PyPsa']['Transmission Flow'],
                                       _scenario[idx],
                                       _years[idx]
                                       )
        elif _p_type[idx] == 'Bar Plot':
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Bar Plot',
                                       data_handler.processed_data['NRCan-PyPsa']['Transmission Flow'],
                                       _scenarios[idx],
                                       _years[idx]
                                       )

        return _canvas, _s_style, _m_style
