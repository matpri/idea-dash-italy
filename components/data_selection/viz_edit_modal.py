import dash_mantine_components as dmc
from dash import html


def render(file):
    from main import data_handler
    # flatten the list of lists
    chip_groups = {}
    for profile, viz_options in data_handler.data[file]['visualizations'].items():
        chips = []
        for viz in viz_options:
            chips.append(dmc.Chip(
                viz,
                value=viz,
                id={'type': 'upload-chip', 'file': file, 'profile': profile, 'viz': viz},
                size='sm',
            ))
        chip_groups[profile] = dmc.ChipGroup(
            children=chips,
            id={'type': 'upload-chip-group', 'file': file, 'profile': profile},
            value=data_handler.data[file]['selected'][profile],
            multiple=True,
            style={'paddingBottom': '4px'}
        )

    layout = dmc.Modal(
        opened=False,
        size='60%',
        id={'type': 'modal', 'index': f'selected-{file}'},
        title=html.H5(f'{file}'),
        zIndex=10001,
        children=[
            dmc.TextInput(
                id={'type': 'upload-scenario-name', 'file': file},
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
                                     id={'type': 'upload-tab', 'file': file, 'profile': profile},
                                     value=profile)
                             for profile in chip_groups.keys()
                             ]
                        ),
                        *[
                            dmc.TabsPanel(
                                children=
                                chip_groups[profile],
                                id={'type': 'upload-tab', 'file': file, 'profile': profile},
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
            html.Div(
            [dmc.Button('Submit', id={'type': 'modal-submit-button', 'index': f'selected-{file}'},
                        variant='gradient'),
             dmc.Button('Close', id={'type': 'modal-close-button', 'index': f'selected-{file}'}, variant='outline'),]
                , style={'display': 'flex', 'justifyContent': 'space-between',
                         'padding': '10px 0px 0px 0px'}
            ),
        ],
    )
    return layout
