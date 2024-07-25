import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_input.visualization_scripts.annual_growth import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'annual_growth'
        }, 'figure'),
        Output({
            'type': 'copper_input-annual_growth-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper_input-annual_growth-year-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'copper_input-annual_growth-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-annual_growth-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-annual_growth-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-annual_growth-year-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'copper_input-annual_growth-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper_input-annual_growth-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'annual_growth'}, 'figure'),
        prevent_initial_call=True
    )
    def update_annual_growth(_p_type, _scenarios, _regions, _years, _r_style, _y_style,
                        _canvas):
        #print('updating annual_growth plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])


        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper_input-annual_growth-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('By Year', data_handler.processed_data['COPPER Input']['Annual Growth'],
                                       _scenarios[idx],
                                       _regions[idx],
                                       _years[idx])



        else:
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('By Region', data_handler.processed_data['COPPER Input']['Annual Growth'],
                                       _scenarios[idx],
                                       _regions[idx],
                                       _years[idx])

        return _canvas, _r_style, _y_style
