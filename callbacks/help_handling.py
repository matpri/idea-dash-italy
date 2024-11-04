import dash
from dash import Input, Output

from components.help import start, load_data, plots, settings, scenario, windows


def link(app: dash.Dash):
    @app.callback(
        Output('help-content', 'children'),
        Input('help-home', 'n_clicks'),
        Input('help-data', 'n_clicks'),
        Input('help-plots', 'n_clicks'),
        Input('help-windows', 'n_clicks'),
        Input('help-settings', 'n_clicks'),
        Input('help-scenario', 'n_clicks'),
    )
    def change_help_content(_home, _data, _plots, _windows, _settings, _scenario):
        """
        Update the help content based on the button clicked.

        This function listens for clicks on various help-related buttons
        and updates the displayed help content accordingly. If no button
        has been clicked, it defaults to rendering the start help content.

        Parameters:
        - _home: Number of clicks on the home help button.
        - _data: Number of clicks on the data help button.
        - _plots: Number of clicks on the plots help button.
        - _windows: Number of clicks on the windows help button.
        - _settings: Number of clicks on the settings help button.
        - _scenario: Number of clicks on the scenario help button.

        Returns:
        - The rendered help content corresponding to the clicked button.
        """
        ctx = dash.callback_context
        if not ctx.triggered:
            return start.render()
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'help-home':
                return start.render()
            elif button_id == 'help-data':
                return load_data.render()
            elif button_id == 'help-plots':
                return plots.render()
            elif button_id == 'help-windows':
                return windows.render()
            elif button_id == 'help-settings':
                return settings.render()
            elif button_id == 'help-scenario':
                return scenario.render()
            else:
                return start.render()