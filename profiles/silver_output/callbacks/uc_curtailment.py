import dash
from dash import Output, Input, State, ALL, dcc

from profiles.silver_output.visualization_scripts.uc_curtailment import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'uc_vre_curtailment'
        }, 'figure'),
        Output({
            'type': 'silver-uc_vre_curtailment-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'silver-uc_vre_curtailment-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'silver-uc_vre_curtailment-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'silver-uc_vre_curtailment-plot-select',
            'index': ALL
        }, 'value'),
        
        Input({
            'type': 'silver-uc_vre_curtailment-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-uc_vre_curtailment-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-uc_vre_curtailment-time_step-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-uc_vre_curtailment-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'uc_vre_curtailment'
        }, 'figure'),
        State({
            'type': 'silver-uc_vre_curtailment-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'silver-uc_vre_curtailment-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'silver-uc_vre_curtailment-scenario-multi-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_uc_vre_curtailment(_p_type, _scenarios, _scenario, _ts, _download, _canvas, _data, _s_style, _m_style):
        print('updating uc_vre_curtailment plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'silver-uc_vre_curtailment-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'silver-uc_vre_curtailment-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['SILVER']['UC_VRE_Curtailment'].to_csv, "uc_vre_curtailment.csv")
            return _canvas, _data, _s_style, _m_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'silver-uc_vre_curtailment-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'Total':
            _m_style[idx] = {'display': 'block'}
            _s_style[idx] = {'display': 'none'}
            _canvas[idx] = render_plot('Total', data_handler.processed_data['SILVER']['UC_VRE_Curtailment'],
                                       _scenarios[idx], time_size=_ts[idx])
        elif _p_type[idx] == 'By Plant':
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('By Plant',
                                       data_handler.processed_data['SILVER']['UC_VRE_Curtailment'],
                                       _scenario[idx], time_size=_ts[idx])
        else:
            _m_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _canvas[idx] = render_plot('By Technology', data_handler.processed_data['SILVER']['UC_VRE_Curtailment'], _scenario[idx], time_size=_ts[idx])

        return _canvas, [dash.no_update for _ in _data], _s_style, _m_style
