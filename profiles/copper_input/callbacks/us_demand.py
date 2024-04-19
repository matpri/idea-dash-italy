import dash
from dash import Output, Input, State, ALL

from profiles.copper_input.visualization_scripts.us_demand import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'us_demand'
        }, 'figure'),
        Output({
            'type': 'copper_input-us_demand-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper_input-us_demand-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper_input-us_demand-region-select',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'copper_input-us_demand-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-us_demand-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-us_demand-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-us_demand-region-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'us_demand'
        }, 'figure'),
        State({
            'type': 'copper_input-us_demand-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper_input-us_demand-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper_input-us_demand-region-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True

    )
    def us_demand_callback(plot_type, scenario_multi_select, _scenario, region_select, figure,
                        scenario_multi_select_style, scenario_select_style, region_select_style):
        from main import data_handler
        ctx = dash.callback_context
        print('updating us_demand plot', ctx.triggered)
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        df = data_handler.processed_data['COPPER Input']['Demand']
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper_input-us_demand-scenario-multi-select')):
                idx = i
                break

        df_scen = df.copy()
        if plot_type[idx] == 'By Scenario':
            df_scen = df_scen[df_scen['scenario'].isin(scenario_multi_select[idx])]
            df_scen = df_scen[df_scen['region'] == region_select[idx]]
            # sort days by month and day
            figure[idx] = render_plot(df_scen, 'By Scenario')
            scenario_multi_select_style[idx] = {'display': 'block'}
            scenario_select_style[idx] = {'display': 'none'}
            region_select_style[idx] = {'display': 'block'}
        else:
            df_scen = df_scen[df_scen['scenario'] == _scenario[idx]]
            figure[idx] = render_plot(df_scen, 'By Region')
            scenario_multi_select_style[idx] = {'display': 'none'}
            scenario_select_style[idx] = {'display': 'block'}
            region_select_style[idx] = {'display': 'none'}

        return figure, scenario_multi_select_style, scenario_select_style, region_select_style
