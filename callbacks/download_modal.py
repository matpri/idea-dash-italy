import dash_mantine_components as dmc
from dash import Output, Input, State, ALL
# download
from dash import dcc
from dash import html
import pandas as pd
import io
import base64
import xlsxwriter
import zipfile
from concurrent.futures import ThreadPoolExecutor
import threading

def link(app):
    app.callback(
        Output('scenario-download-container', 'children'),
        Input('download-scenario-select', "value"),
        prevent_initial_call=True,
    )(toggle_selection)

    app.callback(
        Output('download-data', 'data'),
        Output('download-selected-button', 'loading'),
        Input('download-selected-button', 'n_clicks'),
        State({'type': 'download-chip-group', 'profile': ALL, 'scenario': ALL}, 'value'),
        State({'type': 'download-chip-group', 'profile': ALL, 'scenario': ALL}, 'id'),
        State('download-scenario-select', 'value'),
        prevent_initial_call=True,
    )(download_selected_data)

    app.callback(
        Output('download-selected-button', 'disabled'),
        Input('download-scenario-select', 'value'),
        prevent_initial_call=False,
    )(update_button_state)

def download_selected_data(n_clicks, chip_values, chip_ids, scenarios):
    print('Download clicked', n_clicks, chip_values, chip_ids, scenarios)
    if n_clicks == 0 or not scenarios:
        return None, False

    from utils.data_state import data_handler
    processed_data = data_handler.processed_data

    # Prepare zipped output
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for scenario in scenarios:
            # Pre-filter all data by scenario once
            scenario_filtered_data = {}
            for profile in processed_data:
                scenario_filtered_data[profile] = {}
                for viz, data in processed_data[profile].items():
                    if 'scenario' in data.columns:
                        filtered = data[data['scenario'] == scenario]
                        if not filtered.empty:
                            scenario_filtered_data[profile][viz] = filtered

            # Collect all sheets to write
            sheets_to_write = []
            for values, chip_id in zip(chip_values, chip_ids):
                if not values:
                    continue
                profile = chip_id['profile']
                chip_scenario = chip_id['scenario']
                if chip_scenario != scenario:
                    continue
                for viz in values:
                    if (profile in scenario_filtered_data and viz in scenario_filtered_data[profile]):
                        filtered_data = scenario_filtered_data[profile][viz]
                        sheet_name = f"{profile}|{viz}"
                        if len(sheet_name) > 31:
                            sheet_name = sheet_name[:31]
                        sheets_to_write.append((sheet_name, filtered_data))

            # Write Excel file for this scenario
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, filtered_data in sheets_to_write:
                    filtered_data.to_excel(writer, sheet_name=sheet_name, index=False)
            output.seek(0)
            zipf.writestr(f"{scenario}_selected_data.xlsx", output.read())
    zip_buffer.seek(0)
    encoded = base64.b64encode(zip_buffer.read()).decode()
    return dict(
        content=encoded,
        filename="selected_data.zip",
        base64=True
    ), False

def toggle_selection(scenarios):
    print('SCENARIOS', scenarios)
    from utils.data_state import data_handler
    processed_data = data_handler.processed_data
    viz_data = {}
    for scenario in scenarios or []:
        viz_data[scenario] = {}
        for profile in processed_data.keys():
            for viz, data in processed_data[profile].items():
                if scenario in data.scenario.unique():
                    if profile not in viz_data[scenario]:
                        viz_data[scenario][profile] = {}
                    viz_data[scenario][profile][viz] = data[data['scenario'] == scenario]
    print(viz_data)
    # Get the first scenario and first profile to set as default selected tab
    first_scenario = list(viz_data.keys())[0] if viz_data else None
    first_profile = list(viz_data[first_scenario].keys())[0] if first_scenario and viz_data[first_scenario] else None
    # Create scenario tabs
    scenario_tabs = []
    scenario_tab_contents = []
    for scenario, profiles in viz_data.items():
        scenario_tabs.append(
            dmc.Tab(
                value=scenario,
                children=scenario
            )
        )
        # Create profile tabs for this scenario
        profile_tabs = []
        profile_tab_contents = []
        for profile, vizs in profiles.items():
            profile_tabs.append(
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
                        id={'type': 'download-chip', 'scenario': scenario, 'profile': profile, 'viz': viz},
                        size='sm',
                    )
                )
            chip_groups = dmc.ChipGroup(
                chips,
                value=[f'{viz}' for viz in vizs.keys()],
                multiple=True,
                id={'type': 'download-chip-group', 'scenario': scenario, 'profile': profile},
            )
            profile_tab_contents.append(
                dmc.TabsPanel(
                    value=profile,
                    children=chip_groups
                )
            )
        scenario_tab_contents.append(
            dmc.TabsPanel(
                value=scenario,
                children=dmc.Tabs(
                    value=first_profile,
                    children=[
                        dmc.TabsList(children=profile_tabs),
                        *profile_tab_contents
                    ]
                )
            )
        )
    return dmc.Tabs(
        value=first_scenario,
        children=[
            dmc.TabsList(children=scenario_tabs),
            *scenario_tab_contents
        ],
    )

def update_button_state(scenarios):
    return not scenarios
