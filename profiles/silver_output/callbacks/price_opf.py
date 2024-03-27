import dash
from dash import Output, Input, State, ALL, dcc

from profiles.silver_output.visualization_scripts.price_opf import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'price_opf'
        }, 'figure'),
        Output({
            'type': 'silver-price_opf-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'silver-price_opf-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'silver-price_opf-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'silver-price_opf-plot-select',
            'index': ALL
        }, 'value'),
        
        Input({
            'type': 'silver-price_opf-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-price_opf-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-price_opf-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'price_opf'
        }, 'figure'),
        State({
            'type': 'silver-price_opf-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'silver-price_opf-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'silver-price_opf-scenario-multi-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_price_opf(_p_type, _scenarios, _scenario, _download, _canvas, _data, _s_style, _m_style):
        print('updating price_opf plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'silver-price_opf-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'silver-price_opf-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['SILVER Output']['Price OPF'].to_csv, "price_opf.csv")
            return _canvas, _data, _s_style, _m_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'silver-price_opf-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'Total':
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('By Year', data_handler.processed_data['SILVER Output']['Price OPF'],
                                       _scenarios[idx])

        else:
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('By Technology', data_handler.processed_data['SILVER Output']['Price OPF'], _scenario[idx])

        return _canvas, [dash.no_update for _ in _data], _s_style, _m_style
