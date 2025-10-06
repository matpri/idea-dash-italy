import dash_mantine_components as dmc
from dash import Output, Input, State, ALL, html
import pandas as pd
import io
import base64
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def create_excel_for_scenario(scenario, selected_data, scenario_filtered_data):
    """Create Excel file for a single scenario in parallel"""
    output = io.BytesIO()
    sheets_to_write = []

    # Collect sheets for this scenario
    for profile, vizs in selected_data[scenario].items():
        for viz in vizs:
            if profile in scenario_filtered_data and viz in scenario_filtered_data[profile]:
                filtered_data = scenario_filtered_data[profile][viz]
                sheet_name = f"{profile}|{viz}"
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                sheets_to_write.append((sheet_name, filtered_data))

    # Write Excel file with compatible parameters
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, filtered_data in sheets_to_write:
            # Use more efficient to_excel parameters
            filtered_data.to_excel(writer, sheet_name=sheet_name, index=False)

    output.seek(0)
    return scenario, output.getvalue()

def download_selected_data(n_clicks, chip_values, chip_ids, scenarios):
    print('Download clicked', n_clicks, chip_values, chip_ids, scenarios)
    if n_clicks == 0 or not scenarios:
        return None, False

    from utils.data_state import data_handler
    processed_data = data_handler.processed_data

    # Build selection mapping more efficiently
    selected_data = {}
    for values, chip_id in zip(chip_values, chip_ids):
        if not values:
            continue
        scenario = chip_id['scenario']
        profile = chip_id['profile']

        if scenario not in selected_data:
            selected_data[scenario] = {}
        if profile not in selected_data[scenario]:
            selected_data[scenario][profile] = []

        selected_data[scenario][profile].extend(values)

    print(f"Selected data structure: {selected_data}")

    # Pre-filter all data by scenarios in one pass (more efficient)
    all_scenario_data = {}
    for scenario in scenarios:
        all_scenario_data[scenario] = {}
        for profile in processed_data:
            all_scenario_data[scenario][profile] = {}
            for viz, data in processed_data[profile].items():
                if 'scenario' in data.columns and scenario in selected_data and profile in selected_data[scenario]:
                    # Use pandas query for faster filtering
                    filtered = data.query(f'scenario == "{scenario}"') if scenario in data.scenario.unique() else pd.DataFrame()
                    if not filtered.empty:
                        all_scenario_data[scenario][profile][viz] = filtered

    print(f"All scenario data keys: {list(all_scenario_data.keys())}")
    for scenario in all_scenario_data:
        total_sheets = sum(1 for profile_vizs in all_scenario_data[scenario].values()
                          for viz_name, viz_data in profile_vizs.items()
                          if not viz_data.empty)
        print(f"Scenario {scenario} has {total_sheets} sheets to write")

    # Create Excel files in parallel
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        # Use ThreadPoolExecutor for parallel Excel creation
        with ThreadPoolExecutor(max_workers=min(4, len(scenarios))) as executor:
            # Submit all scenarios for parallel processing
            future_to_scenario = {
                executor.submit(create_excel_for_scenario, scenario, selected_data, all_scenario_data[scenario]): scenario
                for scenario in scenarios if scenario in selected_data
            }

            # Collect results as they complete
            files_created = 0
            for future in as_completed(future_to_scenario):
                scenario = future_to_scenario[future]
                try:
                    scenario_name, excel_data = future.result()
                    if excel_data:  # Only add if there's actual data
                        zipf.writestr(f"{scenario_name}_selected_data.xlsx", excel_data)
                        files_created += 1
                        print(f"Successfully created Excel file for scenario: {scenario_name}")
                    else:
                        print(f"No data to write for scenario: {scenario_name}")
                except Exception as exc:
                    print(f'Scenario {scenario} generated an exception: {exc}')
                    import traceback
                    traceback.print_exc()

    print(f"Total files created in zip: {files_created}")
    zip_buffer.seek(0)

    if files_created == 0:
        print("Warning: No files were created - zip will be empty")
        return None, False

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

    if not scenarios:
        return html.Div()

    viz_data = {}
    # Use set operations for faster scenario checking
    scenario_set = set(scenarios)

    for scenario in scenarios:
        viz_data[scenario] = {}
        for profile in processed_data.keys():
            for viz, data in processed_data[profile].items():
                # More efficient scenario checking using sets
                if 'scenario' in data.columns:
                    unique_scenarios = set(data.scenario.unique())
                    if scenario in unique_scenarios:
                        if profile not in viz_data[scenario]:
                            viz_data[scenario][profile] = {}
                        # Only store reference, don't filter data here for UI performance
                        viz_data[scenario][profile][viz] = True

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
            for viz in vizs.keys():
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
