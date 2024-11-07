import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ALL
from components import ids
from utils import constants
from utils.constants import model_mapping

# Mapping of profile names to their respective module paths
profile_modules = {
    'COPPER': 'profiles.copper_output',
    'COPPER Input': 'profiles.copper_input',
    'SILVER': 'profiles.silver_output',
    'Canada Energy Futures': 'profiles.cef',
    'ECCC-NextGrid': 'profiles.nextgrid_output',
    'NATEM Canada': 'profiles.natem_output',
    'ESMIA-PITHOS': 'profiles.pithos_output',
    'NRCAN-PyPsa': 'profiles.pypsa_output',
    'Power System Models': 'profiles.energy_model',
}

def link(app):
    """
    Link the callbacks to the Dash app for handling data viewer interactions.

    :param app: The Dash app instance
    """
    # Callback to update the chips based on the selected profile
    app.callback(
        Output('view-data-div', 'children'),
        Output('remove-data', 'disabled'),
        Output(ids.AFTER_CHANGE, 'n_clicks'),
        Output('profile-select', 'value', allow_duplicate=True),
        Output('profile-select', 'data', allow_duplicate=True),
        Input('profile-select', 'value'),
        Input('remove-data', 'n_clicks'),
        State(ids.AFTER_CHANGE, 'n_clicks'),
        State('profile-select', 'data'),
        prevent_initial_call=True,
    )(update_chips)

    # Combined callback to manage the data viewer modal state and handle data submission
    app.callback(
        Output('data-viewer-data-modal', 'opened'),
        Output(ids.AFTER_CHANGE, 'n_clicks', allow_duplicate=True),  # Allow duplicate output
        Input('data-viewer', 'n_clicks'),
        Input('submit-data', 'n_clicks'),
        Input('cancel-data', 'n_clicks'),
        State('data-viewer-data-modal', 'opened'),
        State({'type': 'data-viewer-chip-group', 'file': ALL, 'profile': ALL}, 'value'),
        State({'type': 'data-viewer-scenario-name', 'file': ALL}, 'value'),
        prevent_initial_call=True,
    )(view_modal)

def update_chips(file, n_remove, n_click, data):
    """
    Update the visualization chips based on the selected file.

    :param file: The selected file for which to update chips
    :return: The layout containing the updated chips and scenario input
    """
    from main import data_handler

    ctx = dash.callback_context

    # if remove button is clicked, return empty layout
    if n_remove is not None and ctx.triggered_id == 'remove-data':
        data_handler.to_delete.append(file)
        # remove the file from the profile select data
        data.remove(file)

        # disable the remove button
        return [], True, dash.no_update if n_click is None else n_click + 1, '', data

    chip_groups = {}

    # Create chip groups for each profile and its visualization options
    for profile, viz_options in data_handler.data[file]['visualizations'].items():
        chips = []
        for viz in viz_options:
            chips.append(dmc.Chip(
                viz,
                value=viz,
                id={'type': 'data-viewer-chip', 'file': file, 'profile': profile, 'viz': viz},
                size='sm',
            ))
        chip_groups[profile] = dmc.ChipGroup(
            children=chips,
            id={'type': 'data-viewer-chip-group', 'file': file, 'profile': profile},
            value=data_handler.data[file]['selected'][profile],
            multiple=True,
            style={'paddingBottom': '4px'}
        )

    # Create the layout for the loading overlay with scenario input and tabs
    layout = dmc.LoadingOverlay(
        html.Div(
            [
                dmc.TextInput(
                    id={'type': 'data-viewer-scenario-name', 'file': file},
                    label='Scenario Name',
                    value=data_handler.data[file]['scenario'],
                    placeholder='Enter Scenario Name',
                    description='Enter a name for the scenario',
                    style={'marginBottom': '10px'}
                ),
                dmc.Divider(),
                html.Div(
                    dmc.Tabs(
                        [
                            dmc.TabsList(
                                [dmc.Tab(profile,
                                         id={'type': 'data-viewer-tab', 'file': file, 'profile': profile},
                                         value=profile)
                                 for profile in chip_groups.keys()]
                            ),
                            *[
                                dmc.TabsPanel(
                                    children=chip_groups[profile],
                                    id={'type': 'data-viewer-tabpanel', 'file': file, 'profile': profile},
                                    value=profile,
                                    style={
                                        'background': 'rgba(47,146,231,0.2)',
                                        'backdrop-filter': 'blur(5px)',
                                        'box-shadow': '0 4 30px 0 rgba(0, 0, 0, 0.5)',
                                        'border': '1px solid rgba(47,146,231, 0.3)',
                                        '-webkit-backdrop-filter': 'blur(5px)',
                                        'padding': '10px 4px 4px 4px'}
                                )
                                for profile in chip_groups.keys()
                            ]
                        ],
                        value=list(chip_groups.keys())[0]
                    ),
                ),
                dmc.Divider(),
            ],
        )
    )

    return layout, False, dash.no_update, dash.no_update, data

def view_modal(n_click, n_submit, n_cancel, is_open, values, scenario_names):
    """
    Manage the state of the data viewer modal and handle data submission.

    :param n_click: Number of clicks on the data viewer button
    :param n_submit: Number of clicks on the submit button
    :param n_cancel: Number of clicks on the cancel button
    :param is_open: Current state of the modal (open/closed)
    :param values: Selected values from the chip groups
    :param scenario_names: Names of the scenarios to be updated
    :return: Updated modal state and click count
    """
    print('update_modal', n_click, n_submit, n_cancel, is_open, values, scenario_names)
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    # If no button was clicked, return the current state
    if not any([n_click, n_submit, n_cancel]):
        return is_open, dash.no_update

    # Toggle modal state if the data viewer button was clicked
    if triggered_input == 'data-viewer':
        return not is_open, dash.no_update

    # Handle data submission
    if triggered_input == 'submit-data':
        from main import data_handler

        # Update selected values for each profile
        for i, ls in enumerate(ctx.states_list[1]):
            chip = ls['id']
            file = chip['file']
            profile = chip['profile']
            data_handler.data[file]['selected'][profile] = values[i]

        # Update scenario names and process data
        for i, ls in enumerate(ctx.states_list[2]):
            file = ls['id']['file']
            og_scenario = data_handler.data[file]['scenario']
            data_handler.data[file]['scenario'] = scenario_names[i]
            profiles = list(data_handler.data[file]['selected'].keys())
            for profile in profiles:
                scenario = scenario_names[i]
                print(profile)
                module = profile_modules.get(profile, None)
                if module is None:
                    continue
                profile_module = __import__(module, fromlist=[profile])
                if profile == 'Power System Models':
                    # For Power System Models, we need to update the scenario name to include the model name to make them unique for comparison between models with the same scenario name
                    model = data_handler.data[file]['content']['model'].unique()[0]
                    scenario = model + '|' + scenario
                    og_scenario = model + '|' + og_scenario
                og_pattern = profile_module.utils.pattern_from_key(og_scenario) # we keep the pattern for the original scenario name to keep the pattern consistent for the same scenario name
                profile_module.utils.pattern_dict[scenario] = og_pattern

        # delete scenarios
        for file in data_handler.to_delete:
            # delete the file from data_handler
            selected = data_handler.data[file]['selected']
            scenario = data_handler.data[file]['scenario']
            model = data_handler.data[file]['content']['model'].unique()[0]
            mapped_model = model

            if model in list(constants.model_mapping.keys()):
                mapped_model = [m for m in model_mapping[model] if m != 'Power System Models'][0]
            else:
                for profile in data_handler.profiles:
                    if model == profile.name:
                        mapped_model = profile.display_name
                        break

            for profile, viz_options in selected.items():
                for viz in viz_options:
                    processed_data = data_handler.processed_data[profile].get(viz)

                    if profile == 'Power System Models':
                        # remove all entries with the scenario in it
                        processed_data = processed_data[processed_data.scenario != mapped_model + '|' + scenario]
                    else:
                        processed_data = processed_data[processed_data.scenario != scenario]
                    data_handler.processed_data[profile][viz] = processed_data

            del data_handler.data[file]
            data_handler.processed.remove(file)

        data_handler.to_delete = []

        # Process the updated data
        data_handler.process_data(reset=False)

        return not is_open, 1 if n_click is None else n_click + 1

    # Handle cancel action
    if triggered_input == 'cancel-data':
        from main import data_handler

        data_handler.to_delete = []
        return not is_open, dash.no_update
    return is_open, dash.no_update
