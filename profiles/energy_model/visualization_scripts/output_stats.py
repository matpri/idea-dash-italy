import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc


def get_contrasting_font_color(rgb_color):
    """Get a contrasting font color (black or white) based on the background color brightness."""
    print(rgb_color)
    r, g, b = [int(x) for x in rgb_color[4:-1].split(',')]
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Brightness formula for RGB
    return '#ffffff' if brightness < 128 else '#000000'

def render_plot(df, year):
    # Create a Plotly table
    db = df.copy()
    db = db[(db.region == 'CAN') & (db.time == year)]

    if 'Min Dispatch' in db['variable'].unique() and 'Max Dispatch' in db['variable'].unique():
        min_days = db[db.variable == 'Min Dispatch']
        max_days = db[db.variable == 'Max Dispatch']

        min_date = pd.DataFrame({'scenario': min_day['scenario'], 'variable': 'Min Dispatch Day', 'value': min_day['date']} for i, min_day in min_days.iterrows())
        max_date = pd.DataFrame({'scenario': max_day['scenario'], 'variable': 'Max Dispatch Day', 'value': max_day['date']} for i, max_day in max_days.iterrows())
        min_dispatch = pd.DataFrame({'scenario': min_day['scenario'], 'variable': 'Min Dispatch Value', 'value': min_day['value']} for i, min_day in min_days.iterrows())
        max_dispatch = pd.DataFrame({'scenario': max_day['scenario'], 'variable': 'Max Dispatch Value', 'value': max_day['value']} for i, max_day in max_days.iterrows())

        # if multiple min/max dispatch dates, append the values together with a comma
        min_date = min_date.groupby(['scenario', 'variable'])['value'].apply(lambda x: ', '.join(x)).reset_index()
        max_date = max_date.groupby(['scenario', 'variable'])['value'].apply(lambda x: ', '.join(x)).reset_index()

        # only keep the first value for min/max dispatch values if there are multiple
        min_dispatch = min_dispatch.groupby(['scenario', 'variable'])['value'].first().reset_index()
        max_dispatch = max_dispatch.groupby(['scenario', 'variable'])['value'].first().reset_index()


        db = db[db.variable != 'Min Dispatch']
        db = db[db.variable != 'Max Dispatch']
        db = pd.concat([db, min_date, max_date, min_dispatch, max_dispatch])

    db = db[['scenario', 'variable', 'value']]


    df_pivot = db.pivot(index='variable', columns='scenario', values='value')


    # fill na with ''
    df_pivot = df_pivot.fillna('')
    # Create a Plotly Table
    header_values = [''] + list(df_pivot.columns)
    cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

    min_value = df['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
    max_value = df['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

    def normalize(value):
        if isinstance(value, (int, float)):
            return (value - min_value) / (max_value - min_value)
        return None

    colors = []

    for col in df_pivot.columns:
        normalized_data = [normalize(val) for val in df_pivot[col]]
        colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value in normalized_data])]


    colors_by_row = [['#ffffff', '#e5eeec' ] * (len(df_pivot.index) //2)] + colors# Determine font colors based on the background color
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
        columnorder = [i+1 for i in range(len(df_pivot.columns) + 1)],
        columnwidth=column_width,
        header=dict(values=header_values,
                    fill_color=['#ffffff', '#248ce6', '#248ce6'],
                    font=dict(color='white'),
                    align='center'),
        cells=dict(values=cell_values,
                   fill_color=colors_by_row,
                   line_color= colors_by_row,
                   font=dict(color=font_colors),

                   align='left'))
    ])

    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    years = df['time'].unique().tolist()


    widget_layout = html.Div([
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'energy_model-output_stats-year-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'energy_model-output_stats-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-output_stats-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(df, years[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'energy_model',
            'viz': 'output_stats'
        },
        style={
            'width': '100%',
            'height': '100%'
        }

    )

    return widget_layout, plot_layout
