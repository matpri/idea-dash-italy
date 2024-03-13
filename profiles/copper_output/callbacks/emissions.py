import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.emissions import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'copper-emissions-canvas',
            'index': ALL}, 'figure'),
        Output({
            'type': 'copper-emissions-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-emissions-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-emissions-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'copper-emissions-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-emissions-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'copper-emissions-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-emissions-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-emissions-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-emissions-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'copper-emissions-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-emissions-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-emissions-canvas',
            'index': ALL}, 'figure'),
        State({
            'type': 'copper-emissions-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_emissions(_p_type, _aggregates, _scenarios, _regions, _years, _download,_r_style, _y_style, _canvas, _data):
        print('updating emissions plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'copper-emissions-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper-emissions-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER Output']['Emissions'].to_csv, "emissions.csv")
            return _canvas, _r_style, _y_style, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-emissions-plot-select')):
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
                                           _years[idx])

        else:
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['COPPER Output']['Emissions'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx],)

        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data]
