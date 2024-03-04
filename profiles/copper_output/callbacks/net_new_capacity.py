import dash
from dash import Output, Input, State, ALL

from profiles.copper_output.visualization_scripts.net_new_capacity import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'copper-netnewcapacity-canvas',
            'index': ALL}, 'figure'),
        Output({
            'type': 'copper-netnewcapacity-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-netnewcapacity-year-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'copper-netnewcapacity-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-netnewcapacity-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'copper-netnewcapacity-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-netnewcapacity-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-netnewcapacity-year-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'copper-netnewcapacity-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-netnewcapacity-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-netnewcapacity-canvas',
            'index': ALL}, 'figure'),
        prevent_initial_call=True
    )
    def update_netnewcapacity(_p_type, _aggregates, _scenarios, _regions, _years, _r_style, _y_style, _canvas):
        print('updating netnewcapacity plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-netnewcapacity-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['COPPER Output']['Net New Capacity'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx],
                                           title='Net New Capacity by Year',
                                           x_axis_label='Year',
                                           y_axis_label='GW')

        else:
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['COPPER Output']['Net New Capacity'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx],
                                           title='Net New Capacity by Region',
                                           x_axis_label='Region',
                                           y_axis_label='GW')

        return _canvas, _r_style, _y_style
