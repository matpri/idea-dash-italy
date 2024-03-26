import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.cost_total import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'cost_total'
        }, 'figure'),
        Output({
            'type': 'copper-cost_total-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-cost_total-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-cost_total-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'copper-cost_total-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-cost_total-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'copper-cost_total-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-cost_total-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'copper-cost_total-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-cost_total-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-cost_total-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-cost_total-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-cost_total-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'copper-cost_total-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-cost_total-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'cost_total'
        }, 'figure'),
        State({
            'type': 'copper-cost_total-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'copper-cost_total-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-cost_total-scenario-multi-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_cost_total(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _download,_r_style, _y_style, _canvas, _data, _s_style, _m_style):
        print('updating cost_total plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'copper-cost_total-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper-cost_total-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER Output']['Total Cost'].to_csv, "cost_total.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-cost_total-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['COPPER Output']['Total Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['COPPER Output']['Total Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['COPPER Output']['Total Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['COPPER Output']['Total Cost'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data], _s_style, _m_style
