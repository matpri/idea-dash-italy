from dash import html
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def create_widgets(df, classes, window_id):

    params_scenario = []
    params_variables = []
    if 'Technology Parameter' in classes:
        params_scenario = df[df['variable'].str.startswith('Technology Parameter')]['scenario'].unique()
        params_variables = df[df['variable'].str.startswith('Technology Parameter')]['variable'].apply(
            lambda x: x.split('|')[1]).unique()

    params_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in params_scenario],
            value=[params_scenario[0]] if len(params_scenario) else [],
            id={
                'type': 'copper-inputs-params-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Variable',
            data=[{'label': variable, 'value': variable} for variable in params_variables],
            value=params_variables[0] if len(params_variables) else '',
            id={
                'type': 'copper-inputs-params-variable-select',
                'index': window_id
            },
        ),
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-params-widget',
            'index': window_id
        }
    )
    return params_widget_layout

def get_contrasting_font_color(rgb_color):
    """Get a contrasting font color (black or white) based on the background color brightness."""
    print(rgb_color)
    r, g, b = [int(x) for x in rgb_color[4:-1].split(',')]
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Brightness formula for RGB
    return '#ffffff' if brightness < 128 else '#000000'


def render(data, _p_scenario):
    data = data[data['scenario'].isin(_p_scenario)]
    if not data.empty:
        # create a table
        data = data[['scenario', 'variable', 'value']]

        df_pivot = data.pivot(index='variable', columns='scenario', values='value')


        df_pivot = df_pivot.fillna('')
        # Create a Plotly Table
        header_values = [''] + list(df_pivot.columns)
        cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

        min_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
        max_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

        def normalize(value):
            if isinstance(value, (int, float)):
                return (value - min_value) / (max_value - min_value)
            return None

        colors = []

        for col in df_pivot.columns:
            normalized_data = [normalize(val) for val in df_pivot[col]]
            colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[
                                     0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value in
                                 normalized_data])]

        colors_by_row = [['#ffffff', '#e5eeec'] * (
                    len(df_pivot.index) // 2)] + colors  # Determine font colors based on the background color
        font_colors = [['#000000'] * len(df_pivot.index)]
        for column in colors:
            font_colors.append([get_contrasting_font_color(color) for color in column])
        # Calculate the width for each column
        column_width = []
        column_width.append(max(df_pivot.index.str.len()) * 8)
        for col in df_pivot.columns:
            column_width.append(max([len(str(col))] + [len(str(val)) for val in df_pivot[col]]) * 8)

        print(column_width)

        # Create Plotly table
        fig = go.Figure(data=[go.Table(
            columnorder=[i + 1 for i in range(len(df_pivot.columns) + 1)],
            columnwidth=column_width,
            header=dict(values=header_values,
                        fill_color=['#ffffff', '#248ce6', '#248ce6'],
                        font=dict(color='white'),
                        align='center'),
            cells=dict(values=cell_values,
                       fill_color=colors_by_row,
                       line_color=colors_by_row,
                       font=dict(color=font_colors),

                       align='left'))
        ])
    else:
        fig = go.Figure()
        # print("No data available, since the results are all zero.")
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="No data available, since the results are all zero.",
            showarrow=False,
            font=dict(
                size=16,
                color="black"
            ),
            align="center",
            valign="middle",
        )


    return fig