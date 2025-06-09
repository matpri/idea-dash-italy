import dash
from dash import Output, Input, State, ALL, dcc

from profiles.cims_output.callbacks import ghg, stock_lcc, requested_quantities
from components import ids


def link(app):
    ghg.link(app)
    stock_lcc.link(app)
    requested_quantities.link(app)

    @app.callback(
        Output({
            'type': 'cims-overview-stocks',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'cims-overview-demand',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'cims-overview-emissions',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'cims-stocks-update',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'cims-demand-update',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'cims-emissions-update',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'cims-overview-tabs-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'cims-overview-stocks',
            'index': ALL
        }, 'style'),
        State({
            'type': 'cims-overview-demand',
            'index': ALL
        }, 'style'),
        State({
            'type': 'cims-overview-emissions',
            'index': ALL
        }, 'style'),
        State({
            'type': 'cims-stocks-update',
            'index': ALL
        }, 'value'),
        State({
            'type': 'cims-demand-update',
            'index': ALL
        }, 'value'),
        State({
            'type': 'cims-emissions-update',
            'index': ALL
        }, 'value'),
        prevent_initial_call=True
    )
    def update_overview(_p_type, _stocks_style, _demand_style, _emissions_style, _stocks_update, _demand_update, _emissions_update):
        # print('updating overview plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    ((id['id']['type'] == 'cims-overview-tabs-select'))
            ):
                idx = i
                break

        _stocks_style[idx] = {'display': 'block'} if _p_type[idx] == 'Technology Stocks' else {'display': 'none'}
        _demand_style[idx] = {'display': 'block'} if _p_type[idx] == 'Energy Demand' else {'display': 'none'}
        _emissions_style[idx] = {'display': 'block'} if _p_type[idx] == 'Emissions' else {'display': 'none'}

        _stocks_update[idx] = not _stocks_update[idx] if _p_type[idx] == 'Technology Stocks' else dash.no_update
        _demand_update[idx] = not _demand_update[idx] if _p_type[idx] == 'Energy Demand' else dash.no_update
        _emissions_update[idx] = not _emissions_update[idx] if _p_type[idx] == 'Emissions' else dash.no_update

        return _stocks_style, _demand_style, _emissions_style, _stocks_update, _demand_update, _emissions_update
