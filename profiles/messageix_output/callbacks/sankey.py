import dash
from dash import Output, Input, State, ALL, dcc

from profiles.messageix_output.visualization_scripts.sankey import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'MESSAGEix-Canada',
            'viz': 'Sankey'
        }, 'figure'),

        Output({
            'type': 'messageix-sankey-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'messageix-sankey-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-sankey-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-sankey-year-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'messageix-sankey-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'messageix-sankey-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'MESSAGEix-Canada',
            'viz': 'Sankey'
        }, 'figure'),
        prevent_initial_call=True
    )
    def update_sankey(_scenario, _regions, _years, _download, _data, _canvas):
        print('updating sankey plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'messageix-sankey-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'messageix-sankey-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['MESSAGEix-Canada']['Sankey'].to_csv,
                                             "sankey.csv")
            return _canvas, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'messageix-sankey-plot-select')):
                idx = i
                break

        _canvas[idx] = render_plot(data_handler.processed_data['MESSAGEix-Canada']['Sankey'],
                                   _scenario[idx],
                                   _regions[idx],
                                   _years[idx])

        return _canvas, [dash.no_update for _ in _data]
