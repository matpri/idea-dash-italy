import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_input.visualization_scripts.demand import render_plot, date_mapper


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'demand'
        }, 'figure'),
        Input({
            'type': 'copper_input-demand-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-demand-region-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'demand'
        }, 'figure'),
        prevent_initial_call=True

    )
    def demand_callback(scenario_multi_select, region_select, figure):
        from main import data_handler
        ctx = dash.callback_context
        print('updating demand plot', ctx.triggered)
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        df = data_handler.processed_data['COPPER Input']['Demand']
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper_input-demand-scenario-multi-select')):
                idx = i
                break

        df_scen = df.copy()
        df_scen = df_scen[df_scen['scenario'].isin(scenario_multi_select[idx])]
        df_scen = df_scen[df_scen['region']==region_select[idx]]
        # sort days by month and day

        figure[idx] = render_plot(df_scen)

        
        return figure
