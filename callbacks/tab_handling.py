import dash
import dash_mantine_components as dmc
from dash import Input, Output, State

from assets.styles import hide_button_style, view_button_style


def link(app):
    """
    Link the tab handling callbacks to the Dash app.

    This module manages the visibility and state of tabs in the Dash application.
    It handles the toggling of tabs and updates the visualization tab content based on user interactions.

    Parameters:
    - app: The Dash application instance.
    """
    @app.callback(
        Output({'type': 'collapse-tabs', 'index': dash.dependencies.ALL}, 'is_open'),
        Output({'type': 'hide-tab', 'index': dash.dependencies.ALL}, 'style'),
        Output({'type': 'view-tab', 'index': dash.dependencies.ALL}, 'style'),
        Input({'type': 'hide-tab', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input({'type': 'view-tab', 'index': dash.dependencies.ALL}, 'n_clicks'),
        State({'type': 'collapse-tabs', 'index': dash.dependencies.ALL}, 'is_open'),
        prevent_initial_call=True,
    )
    def toggle_tab(n_hide, n_view, is_open):
        """
        Toggle the visibility of tabs based on user clicks.

        Parameters:
        - n_hide: Number of clicks on hide tabs.
        - n_view: Number of clicks on view tabs.
        - is_open: Current state of the tabs (open or closed).

        Returns:
        - Updated state of the tabs and their styles.
        """
        print('toggling tab')
        ctx = dash.callback_context
        triggered_input = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        if triggered_input['type'] == 'hide-tab':
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == triggered_input['index']:
                    is_open[i] = False
        if triggered_input['type'] == 'view-tab':
            for i, out in enumerate(ctx.outputs_list[0]):
                if out['id']['index'] == triggered_input['index']:
                    is_open[i] = True
        hide_style = []
        view_style = []
        for i, open in enumerate(is_open):
            if open:
                hide_style.append(view_button_style)
                view_style.append(hide_button_style)
            else:
                hide_style.append(hide_button_style)
                view_style.append(view_button_style)
        print(is_open, hide_style, view_style, triggered_input, n_hide, n_view, )
        return is_open, hide_style, view_style

    @app.callback(
        Output({'type': 'viz-tab-container', 'index': dash.dependencies.ALL}, 'children'),
        Input({'type': 'profile-tabs', 'index': dash.dependencies.ALL}, 'value'),
        State({'type': 'viz-tab-container', 'index': dash.dependencies.ALL}, 'children'),
        prevent_initial_call=True,
    )
    def display_viz_tab(_tabs, _children):
        """
        Display the visualization tab based on the selected profile.

        Parameters:
        - _tabs: The currently selected tabs.
        - _children: Current children of the visualization tab container.

        Returns:
        - Updated children of the visualization tab container.
        """
        from main import data_handler

        profiles = data_handler.get_viz_options()

        if not profiles:
            return dash.no_update

        ctx = dash.callback_context
        triggered_id = ctx.triggered_id
        triggered_value = ctx.triggered[0]['value']

        viz_options = profiles[triggered_value]

        plots = [plot_option for plot_option in data_handler.profiles[triggered_value].plot_order if plot_option in viz_options]
        viz_tab_list = []
        for viz_type in plots:
            viz_tab_list.append(
                dmc.Tab(
                    dmc.Tooltip(
                        multiline=True,
                        withArrow=True,
                        transition="fade",
                        transitionDuration=200,
                        label=data_handler.profiles[triggered_value].viz_options[viz_type].get('description', ''),
                        children=[viz_type]
                    ),
                    id={'type': 'viz-tab', 'index': triggered_id['index'], 'profile': triggered_value,
                        'viz': viz_type},
                    value=viz_type,
                )
            )
        viz_tab = dmc.Tabs([
            dmc.TabsList(
                [
                    *viz_tab_list
                ]
            )
        ],
            value=plots[0],
            id={'type': 'viz-tabs', 'index': triggered_id['index'], 'profile': triggered_value}
        )


        for i, out in enumerate(ctx.outputs_list):
            if out['id']['index'] == triggered_id['index']:
                _children[i] = viz_tab

        return _children

    @app.callback(
        Output({'type': 'drawer-content', 'index': dash.dependencies.ALL}, 'children'),
        Output({'type': 'hidden_plot', 'index': dash.dependencies.ALL}, 'children'),
        Input({'type': 'viz-tabs', 'index': dash.dependencies.ALL, 'profile': dash.dependencies.ALL}, 'value'),
        State({'type': 'drawer-content', 'index': dash.dependencies.ALL}, 'children'),
        State({'type': 'hidden_plot', 'index': dash.dependencies.ALL}, 'children'),
        prevent_initial_call=True,
    )
    def update_drawer(_values, _children, _plots):
        """
        Update the drawer content based on the selected visualization tab.

        Parameters:
        - _values: Selected values from the visualization tabs.
        - _children: Current children of the drawer content.
        - _plots: Current hidden plots.

        Returns:
        - Updated children of the drawer content and hidden plots.
        """
        from main import data_handler
        ctx = dash.callback_context
        if not ctx.triggered:
            print("No trigger, drawer")
            return dash.no_update

        print('Updating drawer')
        triggered_id = ctx.triggered_id
        triggered_value = ctx.triggered[0]['value']
        for i, out in enumerate(ctx.outputs_list[0]):
            if out['id']['index'] == triggered_id['index']:
                profile = triggered_id['profile']
                viz = triggered_value
                desc = 'DEFAULT'
                for _, report in data_handler.reports.items():
                    if profile in report.descriptions:
                        desc = report.descriptions[profile].get(viz, None)
                window_id = triggered_id['index']
                widgets, plot = data_handler.get_viz(profile, viz, window_id)

                print('DESC:', desc)
                #update plot title with a sub heading with description
                if desc is not None:
                    try:
                        title = plot.figure.layout.title.text
                    except:
                        title = ''

                    if title is None:
                        title = ''

                    plot.figure.update_layout(title_text= title + f"<br>{desc}")

                _children[i] = widgets
                _plots[i] = plot
        return _children, _plots
