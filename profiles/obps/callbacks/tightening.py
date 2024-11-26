import dash
from dash import Output, Input, State, ALL, dcc

from profiles.obps.visualization_scripts.tightening import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'obps',
            'viz': 'tightening'
        }, 'figure'),
        Output({
            'type': 'obps-tightening-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'obps-tightening-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'obps-tightening-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'obps-tightening-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'obps-tightening-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-tightening-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-tightening-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-tightening-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-tightening-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-tightening-sector-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-tightening-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'obps-tightening-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'obps',
            'viz': 'tightening'
        }, 'figure'),
        State({
            'type': 'obps-tightening-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'obps-tightening-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'obps-tightening-scenario-multi-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_tightening(_p_type, _scenarios, _scenario, _regions, _years, _sector,
                         _download, _y_style, _canvas, _data, _s_style, _m_style):
        #print('updating tightening plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'obps-tightening-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'obps-tightening-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['OBPS']['Tightening'].to_csv, "tightening.csv")
            return _canvas, _y_style, _data, _s_style, _m_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'obps-tightening-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'Table':
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}

            _canvas[idx] = render_plot('Table', data_handler.processed_data['OBPS']['Tightening'],
                                       _scenarios[idx],
                                       _regions[idx],
                                       _years[idx],
                                       _sector[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['OBPS']['Tightening'],
                                       _scenario[idx],
                                       _regions[idx],
                                       _years[idx],
                                       _sector[idx])


        return _canvas, _y_style, [dash.no_update for _ in _data], _s_style, _m_style
