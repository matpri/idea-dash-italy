import dash
from dash import Output, Input, State, ALL, dcc

from profiles.obps.visualization_scripts.standard import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'OBPS',
            'viz': 'standard'
        }, 'figure'),
        Output({
            'type': 'obps-standard-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'obps-standard-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'obps-standard-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'obps-standard-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'obps-standard-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-standard-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-standard-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-standard-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-standard-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-standard-sector-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'obps-standard-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'obps-standard-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'OBPS',
            'viz': 'standard'
        }, 'figure'),
        State({
            'type': 'obps-standard-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'obps-standard-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'obps-standard-scenario-multi-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_standard(_p_type, _scenarios, _scenario, _regions, _years, _sector,
                         _download, _y_style, _canvas, _data, _s_style, _m_style):
        #print('updating standard plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'obps-standard-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'obps-standard-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['OBPS']['Standard'].to_csv, "standard.csv")
            return _canvas, _y_style, _data, _s_style, _m_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'obps-standard-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'Table':
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}

            _canvas[idx] = render_plot('Table', data_handler.processed_data['OBPS']['Standard'],
                                       _scenarios[idx],
                                       _regions[idx],
                                       _years[idx],
                                       _sector[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['OBPS']['Standard'],
                                       _scenario[idx],
                                       _regions[idx],
                                       _years[idx],
                                       _sector[idx])


        return _canvas, _y_style, [dash.no_update for _ in _data], _s_style, _m_style
