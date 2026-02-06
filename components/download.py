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
        closeOnClickOutside=True,
        withCloseButton=True,
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
                        dcc.Download(id='download-data'),  # Download component for triggering downloads
                        # Store components for file data and download state
                        dcc.Store(id='download-files-store', data=[]),  # Stores list of files ready for download (remaining files)
                        dcc.Store(id='download-state-store', data={'current_index': 0, 'total_files': 0}),  # Tracks download progress
                        # Interval component for sequential downloads (disabled by default)
                        dcc.Interval(
                            id='download-interval',
                            interval=500,  # 500ms between downloads
                            disabled=True,  # Disabled until download starts
                            n_intervals=0
                        )
                    ],
                        style={'marginTop': '10px', 'marginBottom': '10px', 'display': 'flex',
                               'flexDirection': 'column',
                               'alignItems': 'flex-start'}
                    ),
                    dmc.Divider(),
                    html.Div(id='scenario-download-container', children=[
                    ])
                ],
                id='download-loading-overlay',
                loaderProps={'variant': 'dots', 'size': 'lg', 'color': 'blue'}
            )
        )
    )
