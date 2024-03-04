import dash
from dash import Output, Input, State, ALL

from profiles.copper_output.visualization_scripts.generation_supply import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'copper-supply-canvas',
            'index': ALL}, 'figure'),
        Output({
            'type': 'copper-supply-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-supply-year-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'copper-supply-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-supply-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'copper-supply-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-supply-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-supply-year-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'copper-supply-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-supply-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-supply-canvas',
            'index': ALL}, 'figure'),
        prevent_initial_call=True
    )
    def update_supply(_p_type, _aggregates, _scenarios, _regions, _years, _r_style, _y_style, _canvas):
        print('updating supply plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-supply-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['COPPER Output']['Emissions'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx],
                                           title='Supply by Year',
                                           x_axis_label='Year',
                                           y_axis_label='MtCO2')

        else:
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['COPPER Output']['Emissions'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx],
                                           title='Supply by Region',
                                           x_axis_label='Region',
                                           y_axis_label='MtCO2')

        return _canvas, _r_style, _y_style
