import dash_mantine_components as dmc
from dash import Output, Input, State, ALL, html
import pandas as pd
import io
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

def link(app):
    app.callback(
        Output('scenario-download-container', 'children'),
        Input('download-scenario-select', "value"),
        prevent_initial_call=True,
    )(toggle_selection)

    app.callback(
        Output('download-data', 'data'),
        Output('download-files-store', 'data'),
        Output('download-state-store', 'data'),
        Output('download-interval', 'disabled'),
        Output('download-loading-overlay', 'visible'),
        Output('download-modal', 'closeOnClickOutside'),
        Output('download-modal', 'withCloseButton'),
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

    # Callback for sequential downloads triggered by Interval
    app.callback(
        Output('download-data', 'data', allow_duplicate=True),
        Output('download-files-store', 'data', allow_duplicate=True),
        Output('download-state-store', 'data', allow_duplicate=True),
        Output('download-interval', 'disabled', allow_duplicate=True),
        Output('download-loading-overlay', 'visible', allow_duplicate=True),
        Output('download-modal', 'closeOnClickOutside', allow_duplicate=True),
        Output('download-modal', 'withCloseButton', allow_duplicate=True),
        Input('download-interval', 'n_intervals'),
        State('download-files-store', 'data'),
        State('download-state-store', 'data'),
        prevent_initial_call=True,
    )(handle_sequential_download)

    # Callback to re-enable modal and hide spinner when downloads complete
    app.callback(
        Output('download-loading-overlay', 'visible', allow_duplicate=True),
        Output('download-modal', 'closeOnClickOutside', allow_duplicate=True),
        Output('download-modal', 'withCloseButton', allow_duplicate=True),
        Input('download-interval', 'disabled'),
        Input('download-state-store', 'data'),
        State('download-files-store', 'data'),
        prevent_initial_call=True,
    )(update_modal_state)

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
    """
    Create all Excel files and prepare them for sequential download.
    Returns the first file to download immediately and stores the rest.
    """
    print('Download clicked', n_clicks, chip_values, chip_ids, scenarios)
    if n_clicks == 0 or not scenarios:
        return None, [], {'current_index': 0, 'total_files': 0}, True, False, True, True

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

    # Create Excel files in parallel and store them as list of dicts
    files_list = []
    with ThreadPoolExecutor(max_workers=min(4, len(scenarios))) as executor:
        # Submit all scenarios for parallel processing
        future_to_scenario = {
            executor.submit(create_excel_for_scenario, scenario, selected_data, all_scenario_data[scenario]): scenario
            for scenario in scenarios if scenario in selected_data
        }

        # Collect results as they complete
        for future in as_completed(future_to_scenario):
            scenario = future_to_scenario[future]
            try:
                scenario_name, excel_data = future.result()
                if excel_data:  # Only add if there's actual data
                    # Encode Excel data as base64
                    encoded = base64.b64encode(excel_data).decode()
                    files_list.append({
                        'filename': f"{scenario_name}_selected_data.xlsx",
                        'data': encoded
                    })
                    print(f"Successfully created Excel file for scenario: {scenario_name}")
                else:
                    print(f"No data to write for scenario: {scenario_name}")
            except Exception as exc:
                print(f'Scenario {scenario} generated an exception: {exc}')
                import traceback
                traceback.print_exc()

    print(f"Total files created: {len(files_list)}")

    if len(files_list) == 0:
        print("Warning: No files were created")
        return None, [], {'current_index': 0, 'total_files': 0}, True, False, True, True

    # Return first file to download immediately, store the rest for sequential downloads
    first_file = files_list[0]
    remaining_files = files_list[1:] if len(files_list) > 1 else []
    
    # Initialize download state (current_index=0 means first file is being downloaded)
    download_state = {
        'current_index': 0,
        'total_files': len(files_list)
    }
    
    # Enable interval if there are more files, show loading spinner
    interval_disabled = len(remaining_files) == 0
    loading_visible = True  # Show spinner during downloads
    
    # Disable modal during download (prevent closing)
    modal_close_on_click = False
    modal_with_close_button = False
    
    # Return first file data for immediate download
    first_file_data = dict(
        content=first_file['data'],
        filename=first_file['filename'],
        base64=True
    ) if first_file else None

    return first_file_data, remaining_files, download_state, interval_disabled, loading_visible, modal_close_on_click, modal_with_close_button

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

def update_modal_state(interval_disabled, download_state, files_store):
    """
    Hide spinner and re-enable modal when downloads are complete.
    """
    # If no download state or no downloads initiated, hide spinner and keep modal enabled
    if not download_state or download_state.get('total_files', 0) == 0:
        return False, True, True
    
    current_index = download_state.get('current_index', 0)
    total_files = download_state.get('total_files', 0)
    
    # Check if all downloads are complete
    # Downloads are complete when:
    # 1. We've processed all files (current_index >= total_files - 1)
    # 2. No files remaining in queue (files_store is empty)
    # 3. Interval is disabled (no more downloads pending)
    is_complete = (
        current_index >= total_files - 1 and
        (not files_store or len(files_store) == 0) and
        interval_disabled
    )
    
    if is_complete:
        return False, True, True  # Hide spinner and re-enable modal
    
    # Keep spinner visible and modal disabled during active downloads
    return True, False, False

def handle_sequential_download(n_intervals, files_store, download_state):
    """
    Handle sequential downloads triggered by Interval component.
    Downloads the next file in the queue and updates state.
    """
    # If no files remaining or invalid state, disable interval and re-enable modal
    if not files_store or not download_state or len(files_store) == 0:
        return None, [], {'current_index': 0, 'total_files': 0}, True, False, True, True
    
    current_index = download_state.get('current_index', 0)
    total_files = download_state.get('total_files', 0)
    
    # Check if we've downloaded all files - hide spinner and re-enable modal
    if current_index >= total_files - 1:
        return None, [], download_state, True, False, True, True
    
    # Get next file to download
    next_file = files_store[0]
    remaining_files = files_store[1:] if len(files_store) > 1 else []
    
    # Update download state (increment index for next file)
    new_state = {
        'current_index': current_index + 1,
        'total_files': total_files
    }
    
    # Prepare file data for download
    file_data = dict(
        content=next_file['data'],
        filename=next_file['filename'],
        base64=True
    )
    
    # Disable interval if this is the last file, otherwise keep modal disabled
    interval_disabled = len(remaining_files) == 0
    # Keep spinner visible and modal disabled during download
    loading_visible = True
    # Re-enable modal when downloads complete
    modal_close_on_click = interval_disabled
    modal_with_close_button = interval_disabled
    
    print(f"Downloading file {current_index + 2} of {total_files}: {next_file['filename']}")
    
    return file_data, remaining_files, new_state, interval_disabled, loading_visible, modal_close_on_click, modal_with_close_button

