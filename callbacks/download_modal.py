import dash_mantine_components as dmc
from dash import Output, Input, State, ALL
# download
from dash import dcc
from dash import html
import pandas as pd
import io
import base64
import xlsxwriter
from concurrent.futures import ThreadPoolExecutor
import threading

def link(app):
    app.callback(
        Output('scenario-download-container', 'children'),
        Input('download-scenario-select', "value"),
        prevent_initial_call=True,
    )(toggle_selection)

    # Add download callback
    app.callback(
        Output('download-data', 'data'),
        Output('download-selected-button', 'loading'),
        Input('download-selected-button', 'n_clicks'),
        State({'type': 'download-chip-group', 'profile': ALL, 'scenario': ALL}, 'value'),
        State({'type': 'download-chip-group', 'profile': ALL, 'scenario': ALL}, 'id'),
        State('download-scenario-select', 'value'),
        prevent_initial_call=True,
    )(download_selected_data)

    # Add callback to enable/disable button based on scenario selection
    app.callback(
        Output('download-selected-button', 'disabled'),
        Input('download-scenario-select', 'value'),
        prevent_initial_call=False,
    )(update_button_state)

def download_selected_data(n_clicks, chip_values, chip_ids, scenario):
    print('Download clicked', n_clicks, chip_values, chip_ids, scenario)
    if n_clicks == 0:
        return None, False

    from utils.data_state import data_handler
    processed_data = data_handler.processed_data

    # Pre-filter all data by scenario once
    scenario_filtered_data = {}
    for profile in processed_data:
        scenario_filtered_data[profile] = {}
        for viz, data in processed_data[profile].items():
            if 'scenario' in data.columns:
                filtered = data[data['scenario'] == scenario]
                if not filtered.empty:
                    scenario_filtered_data[profile][viz] = filtered

    # Create Excel writer object in memory using xlsxwriter (faster)
    output = io.BytesIO()

    # Collect all sheets to write
    sheets_to_write = []
    for values, chip_id in zip(chip_values, chip_ids):
        if not values:  # Skip if no chips are selected in this group
            continue

        profile = chip_id['profile']

        # Get data for each selected visualization
        for viz in values:
            if (profile in scenario_filtered_data and
                    viz in scenario_filtered_data[profile]):

                filtered_data = scenario_filtered_data[profile][viz]

                # Create sheet name as profile|viz
                sheet_name = f"{profile}|{viz}"
                # Excel sheet names have a 31 character limit
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]

                sheets_to_write.append((sheet_name, filtered_data))

    # Use xlsxwriter for better performance
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
       # Write sheets sequentially (xlsxwriter doesn't support concurrent writing)
       for sheet_name, filtered_data in sheets_to_write:
           print('Writing sheet:', sheet_name)
           filtered_data.to_excel(writer, sheet_name=sheet_name, index=False)

    output.seek(0)

    # Encode for download
    encoded = base64.b64encode(output.read()).decode()

    return dict(
        content=encoded,
        filename=f"{scenario}_selected_data.xlsx",
        base64=True
    ), False

def toggle_selection(scenario):
    print('SCENARIO', scenario)
    from utils.data_state import data_handler

    processed_data = data_handler.processed_data
    viz_data = {}
    for profile in processed_data.keys():
       for viz, data in processed_data[profile].items():
           if scenario in data.scenario.unique():
               if profile not in viz_data:
                   viz_data[profile] = {}
               viz_data[profile][viz] = data[data['scenario'] == scenario]
    print(viz_data)

    # Get the first profile to set as default selected tab
    first_profile = list(viz_data.keys())[0] if viz_data else None

    # create tabs for each profile
    tabs = []
    # in each tab create selectable chip group
    tab_contents = []

    for profile, vizs in viz_data.items():
        tabs.append(
            dmc.Tab(
                value=profile,
                children=profile
            )
        )

        chips = []
        for viz, data in vizs.items():
            chips.append(
                dmc.Chip(
                    viz,
                    value=f'{viz}',
                    id ={'type': 'download-chip', 'profile': profile, 'viz': viz, 'scenario': scenario},
                    size='sm',
                )
            )
        chip_groups = dmc.ChipGroup(
            chips,
            value =[f'{viz}' for viz in vizs.keys()],
            multiple=True,
            id={'type': 'download-chip-group', 'profile': profile, 'scenario': scenario},
        )

        tab_contents.append(
            dmc.TabsPanel(
                value=profile,
                children=chip_groups
            )
        )

    return dmc.Tabs(
        value=first_profile,  # Set the first tab as selected by default
        children=[
            dmc.TabsList(children=tabs),
            *tab_contents,
        ],
    )

def update_button_state(scenario):
    # Disable the button if no scenario is selected
    return scenario is None or scenario == ''
