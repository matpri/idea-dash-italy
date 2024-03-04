import dash
from dash import Input, Output, State, ALL

from test.utils import bar_over_years, bar_over_regions


def link(app):
    @app.callback(
        Output({'type': 'year-plot-options', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'style'),
        # Output({'type': 'region-plot-options', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'style'),
        Output({'type': 'plot', 'index': ALL}, 'children'),
        Input({'type': 'plot-select', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'value'),
        Input({'type': 'aggregate-switch', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'checked'),
        Input({'type': 'scenario-multi-select', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'value'),
        Input({'type': 'region-select', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'value'),
        Input({'type': 'year-slider', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'value'),
        State({'type': 'year-plot-options', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'style'),
        # State({'type': 'region-plot-options', 'index': ALL, 'profile': dash.dependencies.ALL, 'viz': ALL}, 'style'),
        State({'type': 'plot', 'index': ALL}, 'children'),
        prevent_initial_call=True
    )
    def display_plot_options(_values, _aggregates, _scenarios, _regions, _years, year_style, plots):
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['profile'] == 'COPPER Output') and
                    (id['id']['viz'] == 'Emissions')):
                idx = i
                break
        if _values[idx] == 'By Year':
            year_style[idx] = {'display': 'block'}
            # region_style[idx] = {'display': 'block'}
            if _aggregates:
                plots[idx] = bar_over_years(
                    _scenarios[idx], _regions[idx], _aggregates[idx],
                    title='Emissions by Year',
                    x_axis_label='Year',
                    y_axis_label='MtCO2')
        else:
            year_style[idx] = {'display': 'block'}
            # region_style[idx] = {'display': 'block'}
            if _aggregates:
                plots[idx] = bar_over_regions(
                    _scenarios[idx], _aggregates[idx], _years[idx],
                    title='Emissions by Region',
                    x_axis_label='Region',
                    y_axis_label='MtCO2')
        return year_style, plots
