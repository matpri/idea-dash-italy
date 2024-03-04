import dash
from dash import Output, Input, State, ALL

from profiles.copper_output.visualization_scripts.transmission_capacity import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'copper-transmissionflow-canvas',
            'index': ALL}, 'figure'),



        Input({
            'type': 'copper-transmissionflow-scenario-multi-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper-transmissionflow-year-select',
            'index': ALL
        }, 'value'),

        State({
            'type': 'copper-transmissionflow-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-transmissionflow-canvas',
            'index': ALL}, 'figure'),
        prevent_initial_call=True
    )
    def update_transmissionflow(_scenarios, _years, _seasons, _canvas):
        print('updating transmissionflow plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if (id['id']['index'] == trigger_id['index']):
                idx = i
                break
        _canvas[idx] = render_plot(data_handler.processed_data['COPPER Output']['Transmission Flow'],
                                   _scenarios[idx],
                                   _years[idx],
                                   title='Transmission Flow by Region')

        return _canvas
