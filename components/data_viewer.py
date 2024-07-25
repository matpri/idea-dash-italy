import dash_mantine_components as dmc
from dash import html


def render():
    from main import data_handler

    layout = dmc.Modal(
        title=dmc.Select(
            id='profile-select',
            label='Select Results:',
            data=list(data_handler.data.keys()),
            value=None,
            style={'marginBottom': '10px'}
        ),
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

    return layout
