import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def render():
    from main import data_handler

    return dmc.Modal(
        title=html.Div([
            dmc.Select(
                id='profile-select',
                label='Select Results:',
                data=list(data_handler.data.keys()),
                value=None,
                style={'marginBottom': '10px'}
            ),
            # add a trash button
            dmc.ActionIcon(DashIconify(icon="carbon:trash-can"),
                           size="lg", id='remove-data', variant='light', color='red',
                           style={'marginLeft': '4px', 'marginTop': '10px', 'marginBottom': '10px', 'alignSelf': 'flex-end'},  # Align to bottom
                           disabled=True),
        ], style={'display': 'flex', 'justifyContent': 'space-between',
                  'padding': '10px 0px 0px 0px'}),
        opened=False,
        size='60%',
        id='data-viewer-data-modal',
        children=dmc.LoadingOverlay([
            html.Div(
                id='view-data-div',
                children=[],
            ),
            dmc.Divider(),
            html.Div(
                [
                    dmc.Button('Submit', id='submit-data', variant='gradient'),
                    dmc.Button('Cancel', id='cancel-data', variant='outline'),
                ],
                style={'display': 'flex', 'justifyContent': 'space-between',
                       'padding': '10px 0px 0px 0px'}
            )]
        )

    )
