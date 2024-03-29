from dash import html
import dash_mantine_components as dmc


# template class for a base profile with parameters: name, visualizations and unimplented function preprocess

class BaseProfile:
    name = 'Base Profile'
    db_name = 'base'
    description = 'A Base profile without any visualizations to define model dashboards'
    viz_options = {}
    data = {}
    plot_order = []
    color = 'gray'
    settings = html.Div(
        [
            dmc.Text('Implement Settings for your profile'),
        ]
    )

    def link(self, app):
        for viz in self.viz_options:
            self.viz_options[viz]['callback'](app)