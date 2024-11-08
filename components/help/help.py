import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from components.help import start


def render(help_popup):
    return dmc.Modal(
        title='Help',
        id={'type': 'modal', 'index': 'help'},
        zIndex=10000,
        size='75%',
        closeOnClickOutside=True,
        opened=help_popup,  # Set the modal to be open if help_popup is True
        children=html.Div(
            dmc.Card(
                children=[
                    dmc.Grid(
                        [
                            dmc.Col(dmc.ActionIcon(DashIconify(icon='carbon:home', height='20px'), color='blue',
                                                   variant='light',
                                                   radius="sm", id='help-home',
                                                   style={"height": '30px'}), span='content'),
                            dmc.Col(dmc.Button('Load Data', color='blue', variant='light', id='help-data', radius="sm",
                                               style={"height": '30px'}, size="lg"), span='content'),
                            dmc.Col(dmc.Button('Plots', color='blue', variant='light', id='help-plots', radius="sm",
                                               style={"height": '30px'}, size="lg"), span='content'),
                            dmc.Col(dmc.Button('Windows', color='blue', variant='light', id='help-windows', radius="sm",
                                               style={"height": '30px'}, size="lg"), span='content'),
                            dmc.Col(
                                dmc.Button('Model Settings', color='blue', variant='light', id='help-settings', radius="sm",
                                           style={"height": '30px'}, size="lg"), span='content'),
                            dmc.Col(
                                dmc.Button('Scenario Settings', color='blue', variant='light', id='help-scenario', radius="sm",
                                           style={"height": '30px'}, size="lg"), span='content'),
                        ], className="button-group",
                        gutter='xs',
                        justify='center',
                        align='center',
                    ),
                    html.Div(
                        children=start.render(),
                        style={'width': '100%', 'height': '100%'},
                        id='help-content')
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": '90%',
                       'margin': 'auto',
                       "padding": "20px",
                       "margin-top": "20px",
                       },
            ),

            style={'width': '100%', 'height': '100%'}
        )
    )
