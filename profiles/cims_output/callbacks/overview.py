import dash
from dash import Output, Input, State, ALL, dcc

from profiles.cims_output.visualization_scripts.overview import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'cims_output',
            'viz': 'overview'
        }, 'figure'),

        Output({
            'type': 'cims-overview-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'cims-overview-scenario-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'cims-overview-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-overview-download-button',
            'index': ALL
        }, 'n_clicks'),
        Input({
            'type': 'cims-overview-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-overview-show-sectors',
            'index': ALL
        }, 'checked'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'cims_output',
            'viz': 'overview'
        }, 'figure'),

        State({
            'type': 'cims-overview-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'cims-overview-scenario-select',
            'index': ALL
        }, 'style'),

        prevent_initial_call=True
    )
    def update_overview(_p_type, _download, _scenario, _show_sectors, _canvas, _data,  _scenario_style):
        # print('updating overview plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'cims-overview-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'cims-overview-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['CIMS']['Overview'].to_csv,
                                             "overview.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    ((id['id']['type'] == 'cims-overview-plot-select') or
                     (id['id']['type'] == 'cims-overview-show-sectors') or
                     (id['id']['type'] == 'cims-overview-scenario-select'))
            ):
                idx = i
                break

        print('idx:', idx, 'trigger_id:', trigger_id, _show_sectors)
        if _show_sectors[idx]:
            _scenario_style[idx] = {'display': 'block'}
        else:
            _scenario_style[idx] = {'display': 'none'}

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['CIMS Output']['Overview'],
                                   show_sectors=_show_sectors[idx], scenario=_scenario[idx])

        return _canvas, [dash.no_update for _ in _data], _scenario_style
