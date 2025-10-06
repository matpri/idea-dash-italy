import dash_mantine_components as dmc
from dash import html, dcc


def render():
    """
    Render the download modal.

    :return: The rendered downloads modal.
    """
    from utils.data_state import data_handler
    scenarios = []
    processed_data = data_handler.processed_data
    for profile in processed_data.keys():
        for vis, data in processed_data[profile].items():
            data_scenarios = data.scenario.unique()
            for scenario in data_scenarios:
                if scenario not in scenarios:
                    scenarios.append(scenario)

    return dmc.Modal(
        title='Download Data',
        opened=False,
        id='download-modal',
        size='70%',
        children=html.Div(
            dmc.LoadingOverlay(
                [
                    html.Div([
                        dmc.MultiSelect(
                            id='download-scenario-select',
                            label='Select Scenario(s)',
                            placeholder='Select Scenario(s)',
                            searchable=True,
                            nothingFound='No options found',
                            data=scenarios,
                            style={'width': '50%'}
                        ),
                        dmc.Button(
                            'Download Selected',
                            id='download-selected-button',
                            n_clicks=0,
                            disabled=True,  # Initially disabled until scenario is selected
                            style={'marginTop': '10px'}
                        ),
                        dcc.Download(id='download-data')  # Add download component
                    ],
                        style={'marginTop': '10px', 'marginBottom': '10px', 'display': 'flex',
                               'flexDirection': 'column',
                               'alignItems': 'flex-start'}
                    ),
                    dmc.Divider(),
                    html.Div(id='scenario-download-container', children=[
                    ])
                ]
            )
        )
    )
