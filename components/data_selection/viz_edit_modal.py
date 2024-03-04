import dash_mantine_components as dmc
from dash import html, Input, Output, ALL, callback


def render(app, file):
    from main import data_handler
    # flatten the list of lists
    chip_groups = []
    for profile, viz_options in data_handler.data[file]['visualizations'].items():
        chips = []
        for viz in viz_options:
            chips.append(dmc.Chip(
                viz,
                value=viz,
                id={'type': 'upload-chip', 'file': file, 'profile': profile, 'viz': viz},
                size='sm',
            ))
        chip_groups.append(dmc.ChipGroup(
            children=chips,
            id={'type': 'upload-chip-group', 'file': file, 'profile': profile},
            value=data_handler.data[file]['selected'][profile],
            multiple=True,
            style={'paddingBottom': '10px'}
        ))

    layout = dmc.Modal(
        opened=False,
        id={'type': 'modal', 'index': f'selected-{file}'},
        title=f'Viewing {file}',
        zIndex=10001,
        children=[
            html.H5(f'{file}'),
            html.Div(
                chip_groups,
            ),
            dmc.TextInput(
                id={'type': 'upload-scenario-name', 'file': file},
                label='Scenario Name',
                value=data_handler.data[file]['scenario'],
                placeholder='Enter Scenario Name',
                style={'marginBottom': '10px'}
            ),
            dmc.Button('Close', id={'type': 'modal-close-button', 'index': f'selected-{file}'}, variant='outline'),
            dmc.Button('Submit', id={'type': 'modal-submit-button', 'index': f'selected-{file}'},
                       variant='gradient'),

        ],
    )
    return layout


def update_chips(values):
    # Running a print statement for each chip group
    for val in values:
        print(val)
