import dash
from dash import Input, Output

from components.help import start, load_data, plots, settings, scenario


def link(app: dash.Dash):
    @app.callback(
        Output('help-content', 'children'),
        Input('help-home', 'n_clicks'),
        Input('help-data', 'n_clicks'),
        Input('help-plots', 'n_clicks'),
        Input('help-settings', 'n_clicks'),
        Input('help-scenario', 'n_clicks'),
    )
    def change_help_content(_home, _data, _plots, _settings, _scenario):
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
            elif button_id == 'help-settings':
                return settings.render()
            elif button_id == 'help-scenario':
                return scenario.render()
            else:
                return start.render()