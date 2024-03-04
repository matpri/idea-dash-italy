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
        return len(custom_order)  # For items not in custom_order, place them at the end


province_short = {
    "British Columbia.a": "BC",
    "Alberta.a": "AB",
    "Saskatchewan.a": "SK",
    "Manitoba.a": "MB",
    "Ontario.a": "ON.a",
    "Ontario.b": "ON.b",
    "Quebec.a": "QC.a",
    "Quebec.b": "QC.b",
    "New Brunswick.a": "NB",
    "Nova Scotia.a": "NS",
    "Prince Edward Island.a": "PE",
    "Newfoundland and Labrador.a": "NL.a",
    "Newfoundland and Labrador.b": "NL.b",
    "Yukon.a": "YT",
    "Northwest Territories.a": "NT",
    "Nunavut.a": "NU",
    "british columbia.a": "BC",
    "alberta.a": "AB",
    "saskatchewan.a": "SK",
    "manitoba.a": "MB",
    "ontario.a": "ON.a",
    "ontario.b": "ON.b",
    "quebec.a": "QC.a",
    "quebec.b": "QC.b",
    "new brunswick.a": "NB",
    "nova scotia.a": "NS",
    "prince edward island.a": "PE",
    "newfoundland and labrador.a": "NL.a",
    "newfoundland and labrador.b": "NL.b",
    "yukon.a": "YT",
    "northwest territories.a": "NT",
    "nunavut.a": "NU",
    "British Columbia": "BC",
    "Alberta": "AB",
    "Saskatchewan": "SK",
    "Manitoba": "MB",
    "Ontario": "ON",
    "Quebec": "QC",
    "New Brunswick": "NB",
    "Nova Scotia": "NS",
    "Prince Edward Island": "PE",
    "Newfoundland and Labrador": "NL",
    "Yukon": "YT",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "british columbia": "BC",
    "alberta": "AB",
    "saskatchewan": "SK",
    "manitoba": "MB",
    "ontario": "ON",
    "ontario.b": "ON.b",
    "quebec": "QC",
    "quebec.b": "QC.b",
    "new brunswick": "NB",
    "nova scotia": "NS",
    "prince edward island": "PE",
    "newfoundland and labrador": "NL",
    "newfoundland and labrador.b": "NL.b",
    "yukon": "YT",
    "northwest territories": "NT",
    "nunavut": "NU"
}

# Generation Capacity Names for cost.xlsx
gen_cap_names = ["Wind_ons", "Wind_ofs", "Solar", "Wind_ons_Recon", "Wind_ofs_Recon", "Solar_Recon",
                 "Hydro Capital Cost", "ROR Hydro Renewal", "Day Hydro Renewal", "Month Hydro Renewal",
                 "New Storage Capacity", "coal_pre2025", "coal_fuelblending_pre2025",
                 "coal_ccs_pre2025",
                 "coal_backup_pre2025",
                 "coal_retire_pre2025",
                 "diesel_pre2025",
                 "diesel_fuelblending_pre2025",
                 "diesel_ccs_pre2025",
                 "diesel_backup_pre2025",
                 "diesel_retire_pre2025",
                 "gasSC_pre2025",
                 "gasSC_fuelblending_pre2025",
                 "gasSC_ccs_pre2025",
                 "gasSC_backup_pre2025",
                 "gasSC_retire_pre2025",
                 "gasCCS_post2025",
                 "gasCC_pre2025",
                 "gasCC_fuelblending_pre2025",
                 "gasCC_ccs_pre2025",
                 "gasCC_backup_pre2025",
                 "gasCC_retire_pre2025",
                 'gascc_retire_pre2025'

                 "diesel_bio_pre2025",
                 "diesel_bio_post2025",
                 'diesel_backup_post2025',
                 'gasSC_rng_pre2025',
                 'gasSC_rng_post2025',
                 'gasSC_backup_post2025',
                 'gasCC_rng_pre2025',
                 'gasCC_rng_post2025',
                 'gasCC_backup_post2025',
                 'gasCC_free_post2025',

                 'gasCG_free_pre2025',
                 'gasCG_free_retire2025',
                 'gasCG_restricted_pre2025',
                 'gasCG_restricted_ccs_pre2025',
                 'gasCG_restricted_rng_pre2025',
                 'gasCG_restricted_backup_pre2025',
                 'gasCG_restricted_retire_pre2025',

                 "nuclear",
                 "nuclear_SMR",
                 "h2blue_CT",
                 "h2green_CT",
                 "biomass"]

# Fixed OM Names for cost.xlsx
fom_names = ["FixedOM Wind_ons", "FixedOM Wind_ofs", "FixedOM Solar", "ROR Hydro Capacity", "Day Hydro Capacity",
             "Month Hydro Capacity", "Fixed_OM.biomass",
             "Fixed_OM.coal_pre2025",
             "Fixed_OM.coal_fuelblending_pre2025",
             "Fixed_OM.coal_ccs_pre2025",
             "Fixed_OM.coal_backup_pre2025",
             "Fixed_OM.coal_retire_pre2025",
             "Fixed_OM.diesel_pre2025",
             "Fixed_OM.diesel_fuelblending_pre2025",
             "Fixed_OM.diesel_ccs_pre2025",
             "Fixed_OM.diesel_backup_pre2025",
             "Fixed_OM.diesel_retire_pre2025",
             "Fixed_OM.h2blue_CT",
             "Fixed_OM.h2green_CT",
             "Fixed_OM.gasSC_pre2025",
             "Fixed_OM.gasSC_fuelblending_pre2025",
             "Fixed_OM.gasSC_ccs_pre2025",
             "Fixed_OM.gasSC_backup_pre2025",
             "Fixed_OM.gasSC_retire_pre2025",
             "Fixed_OM.gasCCS_post2025",
             "Fixed_OM.gasCC_pre2025",
             "Fixed_OM.gasCC_fuelblending_pre2025",
             "Fixed_OM.gasCC_ccs_pre2025",
             "Fixed_OM.gasCC_backup_pre2025",
             "Fixed_OM.gasCC_retire_pre2025",
             "Fixed_OM.nuclear",
             "Fixed_OM.nuclear_SMR",
             "Fixed_OM.diesel_bio_pre2025",
             "Fixed_OM.diesel_bio_post2025",
             'Fixed_OM.diesel_backup_post2025',
             'Fixed_OM.gasSC_rng_pre2025',
             'Fixed_OM.gasSC_rng_post2025',
             'Fixed_OM.gasSC_backup_post2025',
             'Fixed_OM.gasCC_rng_pre2025',
             'Fixed_OM.gasCC_rng_post2025',
             'Fixed_OM.gasCC_backup_post2025',
             ]

# Variable OM Names for cost.xlsx
vom_names = ["Wind_ons Out", "Wind_ofs Out", "Solar Out", "ROR Hydro Out", "Day Hydro Out",
             "Month Hydro Out", "Variable_OM.biomass",
             "Variable_OM.coal_pre2025",
             "Variable_OM.coal_fuelblending_pre2025",
             "Variable_OM.coal_ccs_pre2025",
             "Variable_OM.coal_backup_pre2025",
             "Variable_OM.coal_retire_pre2025",
             "Variable_OM.diesel_pre2025",
             "Variable_OM.diesel_fuelblending_pre2025",
             "Variable_OM.diesel_ccs_pre2025",
             "Variable_OM.diesel_backup_pre2025",
             "Variable_OM.diesel_retire_pre2025",
             "Variable_OM.h2blue_CT",
             "Variable_OM.h2green_CT",
             "Variable_OM.gasSC_pre2025",
             "Variable_OM.gasSC_fuelblending_pre2025",
             "Variable_OM.gasSC_ccs_pre2025",
             "Variable_OM.gasSC_backup_pre2025",
             "Variable_OM.gasSC_retire_pre2025",
             "Variable_OM.gasCCS_post2025",
             "Variable_OM.gasCC_pre2025",
             "Variable_OM.gasCC_fuelblending_pre2025",
             "Variable_OM.gasCC_ccs_pre2025",
             "Variable_OM.gasCC_backup_pre2025",
             "Variable_OM.gasCC_retire_pre2025",
             "Variable_OM.nuclear",
             "Variable_OM.nuclear_SMR",
             "Variable_OM.diesel_bio_pre2025",
             "Variable_OM.diesel_bio_post2025",
             'Variable_OM.diesel_backup_post2025',
             'Variable_OM.gasSC_rng_pre2025',
             'Variable_OM.gasSC_rng_post2025',
             'Variable_OM.gasSC_backup_post2025',
             'Variable_OM.gasCC_rng_pre2025',
             'Variable_OM.gasCC_rng_post2025',
             'Variable_OM.gasCC_backup_post2025',
             ]

cost_type = {
    "Capacity cost minus ITC": "capacity_cost_minus_ITC",
    "capacity_cost": "Capacity",
    "carbon_tax_cost": "Carbon_Tax",
    "fom_cost": "Fixed_OM",
    "fuel_cost_weighted": "Fuel",
    "Transmission_capacity_cost": "Transmission",
    "transmission_capacity_cost": "Transmission",
    "variable_om_cost_weighted": "Variable_OM",
    "VRE integration cost": "VRE_Integration"
}


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
    layout = html.Div([
        dmc.Text(
            f'{tech} Settings'
        ),
        dmc.Grid(
            columns=2,
            children=[
                dmc.Col([
                    dmc.TextInput(
                        label='Unaggregated Name',
                        value=names[tech],
                        id={'type': 'copper-tech-name', 'index': tech}
                    ),
                    daq.ColorPicker(
                        value={'hex': colors[tech]},
                        id={'type': 'copper-tech-color', 'index': tech}
                    )]
                ),
                dmc.Col([
                    dmc.TextInput(
                        label='Group Name',
                        value=groups[tech],
                        id={'type': 'copper-tech-group', 'index': tech}
                    ),
                    daq.ColorPicker(
                        value={'hex': group_colors[groups[tech]]},
                        id={'type': 'copper-tech-group-color', 'index': tech}
                    )]
                )
            ]
        ),
        dmc.Button('Update', id={'type': 'copper-tech-update', 'index': tech},
                   disabled=True)
    ])

    return layout


plot_settings = {}


def plot_edit(plot):
    plots = plot_settings[plot]
    types = list(plots.keys())
    views = []
    for i, plot_type in enumerate(types):
        views.append(html.Div([
            dmc.Text(
                f'{plot_type} Settings'
            ),
            dmc.TextInput(
                label='Title',
                value=plots[plot_type]['title'],
                id={'type': 'copper-plot-title', 'index': plot, 'subtype': plot_type}
            ),
            dmc.TextInput(
                label='Y Axis Label',
                value=plots[plot_type]['y_label'],
                id={'type': 'copper-plot-y-axis', 'index': plot, 'subtype': plot_type}
            ),
            dmc.TextInput(
                label='X Axis Label',
                value=plots[plot_type]['x_label'],
                id={'type': 'copper-plot-x-axis', 'index': plot, 'subtype': plot_type}
            ),
            dmc.Divider(),
        ])
        )


    layout = html.Div([
        *views,
        dmc.Button('Update', id={'type': 'copper-plot-update', 'index': plot, 'subtype': '-'.join(types)},
                   disabled=True)
    ])

    return layout
