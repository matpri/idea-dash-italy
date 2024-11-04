from io import StringIO
from random import randint

import dash_daq as daq
import dash_mantine_components as dmc
from dash import html

province_long = {
    'BC': 'British Columbia',
    'AB': 'Alberta',
    'SK': 'Saskatchewan',
    'MB': 'Manitoba',
    'ON': 'Ontario',
    'QC': 'Quebec',
    'NB': 'New Brunswick',
    'NS': 'Nova Scotia',
    'PE': 'Prince Edward Island',
    'NL': 'Newfoundland and Labrador',
    'YT': 'Yukon',
    'NT': 'Northwest Territories',
    'NU': 'Nunavut'
}

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
    return groups.get(key, None)


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
                    id={'type': 'messageix-tech-name', 'index': tech}
                ),
                daq.ColorPicker(
                    value={'hex': colors[tech]},
                    id={'type': 'messageix-tech-color', 'index': tech}
                )],
                style=glass_style
            ),
            html.Div([
                dmc.TextInput(
                    label='Aggregated',
                    value=groups[tech],
                    id={'type': 'messageix-tech-group', 'index': tech}
                ),
                daq.ColorPicker(
                    value={'hex': group_colors[groups[tech]]},
                    id={'type': 'messageix-tech-group-color', 'index': tech}
                )],
                style=glass_style
            )
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),
        html.Div(
            dmc.Button('Update', id={'type': 'messageix-tech-update', 'index': tech}, disabled=True,
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
                id={'type': 'messageix-plot-title', 'index': plot, 'subtype': plot_type}
            ),
            dmc.TextInput(
                label='Y Axis Label',
                value=plots[plot_type]['y_label'],
                id={'type': 'messageix-plot-y-axis', 'index': plot, 'subtype': plot_type}
            ),
            dmc.TextInput(
                label='X Axis Label',
                value=plots[plot_type]['x_label'],
                id={'type': 'messageix-plot-x-axis', 'index': plot, 'subtype': plot_type}
            ),
            dmc.Divider(),
        ],
            style=glass_style
        )
        )

    layout = html.Div([
        *views,
        html.Div(
            dmc.Button('Update', id={'type': 'messageix-plot-update', 'index': plot, 'subtype': '-'.join(types)},
                       disabled=True,
                       style={'display': 'flex', 'justifyContent': 'center', 'width': '80%'}),
            style={'display': 'flex', 'justifyContent': 'center'}
        )

    ])

    return layout