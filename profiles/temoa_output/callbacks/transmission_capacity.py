import dash
from dash import Output, Input, State, ALL, dcc

from profiles.temoa_output.visualization_scripts.transmission_capacity import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'temoa_output',
            'viz': 'transmission_capacity'
        }, 'figure'),
        Output({
            'type': 'temoa-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'temoa-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'temoa-transmissioncapacity-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'temoa-transmissioncapacity-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'temoa-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-transmissioncapacity-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-transmissioncapacity-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'temoa_output',
            'viz': 'transmission_capacity'
        }, 'figure'),
        State({
            'type': 'temoa-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'temoa-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'temoa-transmissioncapacity-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_transmissioncapacity(_p_type, _scenarios, _scenario, _years, _d_button, _canvas, _s_style, _m_style, _data):
        #print('updating transmissioncapacity plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'temoa-transmissioncapacity-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'temoa-transmissioncapacity-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Sutubra-TEMOA']['Transmission Capacity'].to_csv, "transmissioncapacity.csv")
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
                                       data_handler.processed_data['Sutubra-TEMOA']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx]
                                       )
        elif _p_type[idx] == 'Bar Plot':
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Bar Plot',
                                       data_handler.processed_data['Sutubra-TEMOA']['Transmission Capacity'],
                                       _scenarios[idx],
                                       _years[idx]
                                       )

        return _canvas, _s_style, _m_style
