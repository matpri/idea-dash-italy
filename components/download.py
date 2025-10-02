import dash_mantine_components as dmc
from dash import html


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
            [
                dmc.Select(
                    id='download-scenario-select',
                    label='Select Scenario',
                    placeholder='Select Scenario',
                    searchable=True,
                    nothingFound='No options found',
                    data=scenarios,
                    style={'width': '50%'}
                ),
                html.Div(id='scenario-download-container', children=[

                ])
            ]
        )
    )
