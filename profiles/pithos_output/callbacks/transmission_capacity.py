import dash
from dash import Output, Input, State, ALL

from profiles.pithos_output.visualization_scripts.transmission_capacity import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'pithos_output',
            'viz': 'transmission_capacity'
        }, 'figure'),
        Output({
            'type': 'pithos-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'pithos-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'pithos-transmissioncapacity-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'pithos-transmissioncapacity-scenario-multi-select',
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
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'pithos_output',
            'viz': 'transmission_capacity'
        }, 'figure'),
        State({
            'type': 'pithos-transmissioncapacity-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'pithos-transmissioncapacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_transmissioncapacity(_p_type, _scenarios, _scenario, _years, _canvas, _s_style, _m_style):
        print('updating transmissioncapacity plot')
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
            _canvas[idx] = render_plot('Map Plot',
                                       data_handler.processed_data['ESMIA-PITHOS Output']['Transmission Capacity'],
                                       _scenario[idx],
                                       _years[idx]
                                       )
        elif _p_type[idx] == 'Bar Plot':
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Bar Plot',
                                       data_handler.processed_data['ESMIA-PITHOS Output']['Transmission Capacity'],
                                       _scenarios[idx],
                                       _years[idx]
                                       )

        return _canvas, _s_style, _m_style
