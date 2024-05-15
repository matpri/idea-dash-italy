from io import StringIO
from random import randint

import dash_daq as daq
import dash_mantine_components as dmc
from dash import html

plotly_pattern_list = ['', '/', 'x', '-', '|', '+', '.', '\\']
pattern_dict = {}


def pattern_from_key(key):
    global pattern_dict
    if key not in pattern_dict:
        pattern_dict[key] = plotly_pattern_list[len(pattern_dict) % len(plotly_pattern_list)]
    return pattern_dict[key]


custom_order = ['Hydro', 'Fossil fuel gas', 'Fossil fuel liquid', 'Fossil fuel solid', 'nuclear', 'wind', 'solar', 'BC',
                'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL']


def custom_sort_key(value):
    try:
        return custom_order.index(value)
    except ValueError:
        custom_order.append(value)
        return len(custom_order)  # For items not in custom_order, place them at the end


def csv2sio(df):
    def func():
        sio = StringIO()
        df.to_csv(sio, index=False)
        sio.seek(0)
        return sio

    return func

colors = {}


def get_color(key):
    global colors
    if key not in colors:
        colors[key] = '#%06X' % randint(0, 0xFFFFFF)

    if colors[key] in ['#000000', '#FFFFFF']:
        colors[key] = '#%06X' % randint(0, 0xFFFFFF)

    return colors[key]


group_colors = {}


def get_group_colors(key):
    global group_colors
    if key not in group_colors:
        group_colors[key] = '#%06X' % randint(0, 0xFFFFFF)

    if group_colors[key] in ['#000000', '#FFFFFF']:
        group_colors[key] = '#%06X' % randint(0, 0xFFFFFF)

    return group_colors[key]


names = {}


def get_name(key):
    global names
    if key not in names:
        names[key] = key
    return names[key]


groups = {}


def get_group(key):
    global groups
    if key not in groups:
        groups[key] = key
    return groups[key]


def tech_edit(tech):
    glass_style = {
        'background': 'rgba(255, 255, 255, 0.4)',
        'backdropFilter': 'blur(20px)',
        'borderRadius': '25px',
        'boxShadow': '10px 10px 15px rgba(0, 0, 0, 0.1)',
        'padding': '2rem',
        'marginTop': '1rem',
        'marginBottom': '1rem',
    }
    layout = html.Div([
        html.Div(children=[
            html.Div([
                dmc.TextInput(
                    label='Unaggregated',
                    value=names[tech],
                    id={'type': 'generic-tech-name', 'index': tech}
                ),
                daq.ColorPicker(
                    value={'hex': colors[tech]},
                    id={'type': 'generic-tech-color', 'index': tech}
                )],
                style=glass_style
            ),
            html.Div([
                dmc.TextInput(
                    label='Aggregated',
                    value=groups[tech],
                    id={'type': 'generic-tech-group', 'index': tech}
                ),
                daq.ColorPicker(
                    value={'hex': group_colors[groups[tech]]},
                    id={'type': 'generic-tech-group-color', 'index': tech}
                )],
                style=glass_style
            )
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),
        html.Div(
            dmc.Button('Update', id={'type': 'generic-tech-update', 'index': tech}, disabled=True,
                       style={'display': 'flex', 'justifyContent': 'center', 'width': '80%'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        )
    ], style={'margin': '2rem'})

    return layout


plot_settings = {}


def plot_edit(plot):
    plots = plot_settings[plot]
    types = list(plots.keys())
    # remove name and unit from types if they exist
    if 'name' in types:
        types.remove('name')
    if 'unit' in types:
        types.remove('unit')

    glass_style = {
        'background': 'rgba(255, 255, 255, 0.4)',
        'backdropFilter': 'blur(20px)',
        'borderRadius': '25px',
        'boxShadow': '10px 10px 15px rgba(0, 0, 0, 0.1)',
        'padding': '2rem',
        'marginBottom': '2rem',
    }

    views = []
    for i, plot_type in enumerate(types):
        views.append(html.Div([
            dmc.Text(
                f'{plot_type} Settings'
            ),
            dmc.TextInput(
                label='Title',
                value=plots[plot_type]['title'],
                id={'type': 'generic-plot-title', 'index': plot, 'subtype': plot_type}
            ),
            dmc.TextInput(
                label='Y Axis Label',
                value=plots[plot_type]['y_label'],
                id={'type': 'generic-plot-y-axis', 'index': plot, 'subtype': plot_type}
            ),
            dmc.TextInput(
                label='X Axis Label',
                value=plots[plot_type]['x_label'],
                id={'type': 'generic-plot-x-axis', 'index': plot, 'subtype': plot_type}
            ),
            dmc.Divider(),
        ],
            style=glass_style
        )
        )

    layout = html.Div([
        *views,
        html.Div(
            dmc.Button('Update', id={'type': 'generic-plot-update', 'index': plot, 'subtype': '-'.join(types)},
                       disabled=True,
                       style={'display': 'flex', 'justifyContent': 'center', 'width': '80%'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        )

    ])

    return layout

# technology names in cost.xlsx
cost_tech = {
    "Wind_ons": "Wind",
    "Wind_ofs": "Wind",
    "Wind_ons Out": "Wind",
    "Wind_ofs Out": "Wind",
    "Wind_ons_Recon": "Wind",
    "Wind_ofs_Recon": "Wind",
    "FixedOM Wind_ons": "Wind",
    "FixedOM Wind_ofs": "Wind",
    "Solar": "Solar",
    "Solar_Recon": "Solar",
    "Solar Out": "Solar",
    "FixedOM Solar": "Solar",
    "Hydro Capital Cost": "Hydro",
    "ROR Hydro Renewal": "Hydro",
    "Day Hydro Renewal": "Hydro",
    "Month Hydro Renewal": "Hydro",
    "ROR Hydro Capacity": "Hydro",
    "Day Hydro Capacity": "Hydro",
    "Month Hydro Capacity": "Hydro",
    "ROR Hydro Out": "Hydro",
    "Day Hydro Out": "Hydro",
    "Month Hydro Out": "Hydro",
    "New Storage Capacity": "Storage",
    "coal_pre2025": "Fossil fuel solid",
    "coal_fuelblending_pre2025": "Fossil fuel solid",
    "coal_ccs_pre2025": "Fossil fuel solid",
    "coal_backup_pre2025": "Fossil fuel solid",
    "coal_retire_pre2025": "Fossil fuel solid",
    "diesel_pre2025": "Fossil fuel liquid",
    "diesel_fuelblending_pre2025": "Fossil fuel liquid",
    "diesel_ccs_pre2025": "Fossil fuel liquid",
    "diesel_backup_pre2025": "Fossil fuel liquid",
    "diesel_retire_pre2025": "Fossil fuel liquid",
    "gasSC_pre2025": "Fossil fuel gas",
    "gasSC_fuelblending_pre2025": "Fossil fuel gas",
    "gasSC_ccs_pre2025": "Fossil fuel gas",
    "gasSC_backup_pre2025": "Fossil fuel gas",
    "gasSC_retire_pre2025": "Fossil fuel gas",
    "gasCCS_post2025": "Fossil fuel gas",
    "gasCC_pre2025": "Fossil fuel gas",
    "gasCC_fuelblending_pre2025": "Fossil fuel gas",
    "gasCC_ccs_pre2025": "Fossil fuel gas",
    "gasCC_backup_pre2025": "Fossil fuel gas",
    "gasCC_retire_pre2025": "Fossil fuel gas",
    "nuclear": "Nuclear",
    "nuclear_SMR": "Nuclear",
    "h2blue_CT": "Hydrogen",
    "h2green_CT": "Hydrogen",
    "biomass": "Biomass",
    "Fixed_OM.biomass": "Biomass",
    "Fixed_OM.h2blue_CT": "Hydrogen",
    "Fixed_OM.h2green_CT": "Hydrogen",
    "Fixed_OM.coal_pre2025": "Fossil fuel solid",
    "Fixed_OM.coal_fuelblending_pre2025": "Fossil fuel solid",
    "Fixed_OM.coal_ccs_pre2025": "Fossil fuel solid",
    "Fixed_OM.coal_backup_pre2025": "Fossil fuel solid",
    "Fixed_OM.coal_retire_pre2025": "Fossil fuel solid",
    "Fixed_OM.diesel_pre2025": "Fossil fuel liquid",
    "Fixed_OM.diesel_fuelblending_pre2025": "Fossil fuel liquid",
    "Fixed_OM.diesel_ccs_pre2025": "Fossil fuel liquid",
    "Fixed_OM.diesel_backup_pre2025": "Fossil fuel liquid",
    "Fixed_OM.diesel_retire_pre2025": "Fossil fuel liquid",
    "Fixed_OM.gasSC_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasSC_fuelblending_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasSC_ccs_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasSC_backup_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasSC_retire_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasCCS_post2025": "Fossil fuel gas",
    "Fixed_OM.gasCC_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasCC_fuelblending_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasCC_ccs_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasCC_backup_pre2025": "Fossil fuel gas",
    "Fixed_OM.gasCC_retire_pre2025": "Fossil fuel gas",
    "Fixed_OM.nuclear": "Nuclear",
    "Fixed_OM.nuclear_SMR": "Nuclear",
    "Fixed_OM.SMR": "Nuclear",

    "Variable_OM.biomass": "Biomass",
    "Variable_OM.h2blue_CT": "Hydrogen",
    "Variable_OM.h2green_CT": "Hydrogen",
    "Variable_OM.coal_pre2025": "Fossil fuel solid",
    "Variable_OM.coal_fuelblending_pre2025": "Fossil fuel solid",
    "Variable_OM.coal_ccs_pre2025": "Fossil fuel solid",
    "Variable_OM.coal_backup_pre2025": "Fossil fuel solid",
    "Variable_OM.coal_retire_pre2025": "Fossil fuel solid",
    "Variable_OM.diesel_pre2025": "Fossil fuel liquid",
    "Variable_OM.diesel_fuelblending_pre2025": "Fossil fuel liquid",
    "Variable_OM.diesel_ccs_pre2025": "Fossil fuel liquid",
    "Variable_OM.diesel_backup_pre2025": "Fossil fuel liquid",
    "Variable_OM.diesel_retire_pre2025": "Fossil fuel liquid",
    "Variable_OM.gasSC_pre2025": "Fossil fuel gas",
    "Variable_OM.gasSC_fuelblending_pre2025": "Fossil fuel gas",
    "Variable_OM.gasSC_ccs_pre2025": "Fossil fuel gas",
    "Variable_OM.gasSC_backup_pre2025": "Fossil fuel gas",
    "Variable_OM.gasSC_retire_pre2025": "Fossil fuel gas",
    "Variable_OM.gasCCS_post2025": "Fossil fuel gas",
    "Variable_OM.gasCC_pre2025": "Fossil fuel gas",
    "Variable_OM.gasCC_fuelblending_pre2025": "Fossil fuel gas",
    "Variable_OM.gasCC_ccs_pre2025": "Fossil fuel gas",
    "Variable_OM.gasCC_backup_pre2025": "Fossil fuel gas",
    "Variable_OM.gasCC_retire_pre2025": "Fossil fuel gas",
    "Variable_OM.nuclear": "Nuclear",
    "Variable_OM.nuclear_SMR": "Nuclear",
    "Variable_OM.SMR": "Nuclear",

    "diesel_bio_pre2025": "Fossil fuel liquid",
    "diesel_bio_post2025": "Fossil fuel liquid",
    "diesel_backup_post2025": "Fossil fuel liquid",
    "hydro_daily": "Hydro",
    "hydro_monthly": "Hydro",
    "hydro_run": "Hydro",
    "h2blue_ct": "Hydrogen",
    "h2green_ct": "Hydrogen",
    "gassc_pre2025": "Fossil fuel gas",
    "gassc_ccs_pre2025": "Fossil fuel gas",
    "gasSC_rng_pre2025": "Fossil fuel gas",
    "gassc_rng_pre2025": "Fossil fuel gas",
    "gassc_backup_pre2025": "Fossil fuel gas",
    "gasSC_rng_post2025": "Fossil fuel gas",
    "gassc_rng_post2025": "Fossil fuel gas",
    "gasSC_backup_post2025": "Fossil fuel gas",
    "gassc_backup_post2025": "Fossil fuel gas",
    "gassc_retire_pre2025": "Fossil fuel gas",

    'gassc_free_retire_pre2025': "Fossil fuel gas",
    "gasccs_post2025": "Fossil fuel gas",
    "gascc_pre2025": "Fossil fuel gas",
    "gascc_ccs_pre2025": "Fossil fuel gas",
    "gasCC_rng_pre2025": "Fossil fuel gas",
    "gascc_rng_pre2025": "Fossil fuel gas",
    "gascc_backup_pre2025": "Fossil fuel gas",
    "gasCC_rng_post2025": "Fossil fuel gas",
    "gascc_rng_post2025": "Fossil fuel gas",
    "gascc_backup_post2025": "Fossil fuel gas",
    'gascc_retire_pre2025': "Fossil fuel gas",
    "gasCC_backup_post2025": "Fossil fuel gas",
    "nuclear_smr": "Nuclear",
    "SMR": "Nuclear",
    "storage_LI": "Storage",
    "storage_PH": "Storage",
    "wind_ons": "Wind",
    "wind_ofs": "Wind",
    "storage_ph": "Storage",
    "storage_li": "Storage",
    "solar": "Solar",
    "Fixed_OM.diesel_bio_pre2025": "Fossil fuel liquid",
    "Fixed_OM.diesel_bio_post2025": "Fossil fuel liquid",
    'Fixed_OM.diesel_backup_post2025': "Fossil fuel liquid",
    'Fixed_OM.gasSC_rng_pre2025': "Fossil fuel gas",
    'Fixed_OM.gasSC_rng_post2025': "Fossil fuel gas",
    'Fixed_OM.gasSC_backup_post2025': "Fossil fuel gas",
    'Fixed_OM.gasCC_rng_pre2025': "Fossil fuel gas",
    'Fixed_OM.gasCC_rng_post2025': "Fossil fuel gas",
    'Fixed_OM.gasCC_backup_post2025': "Fossil fuel gas",

    "Variable_OM.diesel_bio_pre2025": "Fossil fuel liquid",
    "Variable_OM.diesel_bio_post2025": "Fossil fuel liquid",
    'Variable_OM.diesel_backup_post2025': "Fossil fuel liquid",
    'Variable_OM.gasSC_rng_pre2025': "Fossil fuel gas",
    'Variable_OM.gasSC_rng_post2025': "Fossil fuel gas",
    'Variable_OM.gasSC_backup_post2025': "Fossil fuel gas",
    'Variable_OM.gasCC_rng_pre2025': "Fossil fuel gas",
    'Variable_OM.gasCC_rng_post2025': "Fossil fuel gas",
    'Variable_OM.gasCC_backup_post2025': "Fossil fuel gas",
    "Variable_OM.gasCC_free_post2025": "Fossil fuel gas",

    'gasCG_free_pre2025': "Fossil fuel gas",
    'gasCG_free_retire2025': "Fossil fuel gas",
    'gasCG_restricted_pre2025': "Fossil fuel gas",
    'gasCG_restricted_ccs_pre2025': "Fossil fuel gas",
    'gasCG_restricted_rng_pre2025': "Fossil fuel gas",
    'gasCG_restricted_backup_pre2025': "Fossil fuel gas",
    'gasCG_restricted_retire_pre2025': "Fossil fuel gas",
    'gascg_restricted_retire_pre2025': "Fossil fuel gas",
    'gascg_restricted_pre2025': "Fossil fuel gas",
    'gasCC_free_post2025': "Fossil fuel gas",
    'gascg_restricted_ccs_pre2025': "Fossil fuel gas",
    'gascg_restricted_rng_pre2025': "Fossil fuel gas",
    'gassc_ccs_post2025': "Fossil fuel gas",
    'FixedOM Transmission': 'Transmission',
    'Extant Transmission': 'Transmission',
}