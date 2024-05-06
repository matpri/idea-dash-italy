import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ALL


from components import ids

profile_modules = {
    'COPPER Output': 'profiles.copper_output',
    'COPPER Input': 'profiles.copper_input',
    'SILVER Output': 'profiles.silver_output',
    'Canada Energy Futures': 'profiles.cef',
    'ECCC-NextGrid Output': 'profiles.nextgrid_output',
    'NATEM-POWER Output': 'profiles.natem_output',
    'ESMIA-PITHOS Output': 'profiles.pithos_output',
    'NRCAN-PyPsa Output': 'profiles.pypsa_output',
    'Power System Models': 'profiles.energy_model',

}

def link(app):
    app.callback(
        Output('view-data-div', 'children'),
        Input('profile-select', 'value'),
        prevent_initial_call=True,
    )(update_chips)

    app.callback(
        Output('data-viewer-data-modal', 'opened'),
        Output(ids.AFTER_CHANGE, 'n_clicks'),
        Input('data-viewer', 'n_clicks'),
        Input('submit-data', 'n_clicks'),
        Input('cancel-data', 'n_clicks'),
        State('data-viewer-data-modal', 'opened'),
        State({'type': 'data-viewer-chip-group', 'file': ALL, 'profile': ALL}, 'value'),
        State({'type': 'data-viewer-scenario-name', 'file': ALL}, 'value'),
        prevent_initial_call=True,
    )(view_modal)


def update_chips(file):
    from main import data_handler
    chip_groups = {}
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
                                 for profile in chip_groups.keys()
                                 ]
                            ),
                            *[
                                dmc.TabsPanel(
                                    children=
                                    chip_groups[profile],
                                    id={'type': 'data-viewer-tabpanel', 'file': file, 'profile': profile},
                                    value=profile,
                                    style={
                                        'background': 'rgba(47,146,231,0.2)',
                                        # 'border-radius': '10px',
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

    return layout


def view_modal(n_click, n_submit, n_cancel, is_open, values, scenario_names):
    print('update_modal', n_click, n_submit, n_cancel, is_open, values, scenario_names)
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    if not any([n_click, n_submit, n_cancel]):
        return is_open, dash.no_update

    if triggered_input == 'data-viewer':
        return not is_open, dash.no_update

    if triggered_input == 'submit-data':
        from main import data_handler
        for i, ls in enumerate(ctx.states_list[1]):
            chip = ls['id']
            file = chip['file']
            profile = chip['profile']
            data_handler.data[file]['selected'][profile] = values[i]
        for i, ls in enumerate(ctx.states_list[2]):
            file = ls['id']['file']
            og_scenario = data_handler.data[file]['scenario']
            data_handler.data[file]['scenario'] = scenario_names[i]
            profiles = list(data_handler.data[file]['selected'].keys())
            for profile in profiles:
                scenario = scenario_names[i]
                print(profile)
                module = profile_modules[profile]
                profile_module = __import__(module, fromlist=[profile])
                if profile == 'Power System Models':
                    model = data_handler.data[file]['content']['model'].unique()[0]
                    scenario = model + '|' + scenario
                    og_scenario = model + '|' + og_scenario
                og_pattern = profile_module.utils.pattern_from_key(og_scenario)
                profile_module.utils.pattern_dict[scenario] = og_pattern

        data_handler.process_data()

        return not is_open, 1 if n_click is None else n_click + 1

    if triggered_input == 'cancel-data':
        return not is_open, dash.no_update

    return is_open, dash.no_update
