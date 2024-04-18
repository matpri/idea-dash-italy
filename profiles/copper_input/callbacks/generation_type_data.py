import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_input.visualization_scripts.generation_type_data import render_plot

def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'gentype'
        }, 'figure'),
        Input({
            'type': 'copper_input-gentype-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-gentype-variable-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'gentype'
        }, 'figure'),
        prevent_initial_call=True

    )
    def generation_type_data_callback(scenario_multi_select, variable_select, figure):
        from main import data_handler
        ctx = dash.callback_context
        print('updating generation type data plot', ctx.triggered)
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        df = data_handler.processed_data['COPPER Input']['Generation Type Data']
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper_input-gentype-scenario-multi-select')):
                idx = i
                break

        scenarios = scenario_multi_select[idx]
        variable = variable_select[idx]

        figure[idx] = render_plot(df, scenarios, variable)

        return figure