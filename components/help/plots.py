import dash_mantine_components as dmc
from dash import html, dcc


def render():
    layout = html.Div([
        html.H1('Change plots'),
        html.P(
            'Every window has a tab bar at the top. The tab bar is nested and contains tabs for every model type that is available in the data, and for every model type there are tabs for every plot option that is available. To change the plot, click on the tab of the model type you want to change. Then click on the tab of the plot option you want to change. The plot will change accordingly.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/plot_change.gif', style={'width': '100%'})),
            html.H3('Changing Plots', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1('Edit plots'),
        html.P(
            'Every plot has widgets to its left that allow you to change the plot, by changing predefined parameters, that include but are not limited to the scenario, the period, the region and the plot type. By changing the parameters, the plot will change accordingly.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/plot_widgets.gif', style={'width': '100%'})),
            html.H3('Editing Plots', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1('Save plots'),
        html.P(
            'To save a plot, click the "Save" button in the top right corner of the plot window. The plot will be saved as a PNG file.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/plot_save.gif', style={'width': '100%'})),
            html.H3('Saving Plots', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1('Change View'),
        html.P(
            'To have a clean interface where only the plot is visible, hide the widgets by clicking the hamburger menu in the top left corner of the window and press the  "^" button to hide the tab bar. To show the widgets or tabs again, click the hamburger menu or the "v" button accordingly.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/plot_hide.gif', style={'width': '100%'})),
            html.H3('Changing View', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

    ])

    return layout