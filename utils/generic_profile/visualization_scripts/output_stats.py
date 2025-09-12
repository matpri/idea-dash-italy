import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

from utils.generic_profile import utils
from components import ids


def get_contrasting_font_color(rgb_color):
    """Get a contrasting font color (black or white) based on the background color brightness."""
    # print(rgb_color)
    r, g, b = [int(x) for x in rgb_color[4:-1].split(',')]
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Brightness formula for RGB
    return '#ffffff' if brightness < 128 else '#000000'


def render_plot(p_type, df, year, model):
    """Render a plot based on the specified plot type, data, year, scenarios, and model."""
    
    # Filter the DataFrame for the relevant data
    db = df[(df.region == 'National') & (df.time == year)].copy()

    if db.empty:
        # Create a figure with a no data available message
        fig = go.Figure()
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="No data available, since the results are all zero.",
            showarrow=False,
            font=dict(size=16, color="black"),
            align="center",
            valign="middle",
        )
        return fig

    if p_type == 'Table':
        # Process Min and Max Dispatch data if available
        min_days = db[db.variable == 'Min Dispatch']
        max_days = db[db.variable == 'Max Dispatch']

        if not min_days.empty and not max_days.empty:
            min_date, max_date, min_dispatch, max_dispatch = process_dispatch_data(min_days, max_days)

            # Remove Min/Max Dispatch from the main DataFrame and concatenate new data
            db = db[~db.variable.isin(['Min Dispatch', 'Max Dispatch'])]
            db = pd.concat([db, min_date, max_date, min_dispatch, max_dispatch])

        # Prepare the DataFrame for the Plotly table
        db = db[['scenario', 'variable', 'value']]
        df_pivot = db.pivot(index='variable', columns='scenario', values='value').fillna('')

        # Create a Plotly Table
        fig = create_plotly_table(df_pivot, df['value'])
    else:
        # Prepare data for scatter plot
        db = db[['scenario', 'variable', 'value']]
        db = db[db['value'].apply(lambda x: isinstance(x, (int, float)))]

        if model == 'Generic Comparison':
            db['m_scen'] = db['scenario'].copy()
            db['model'], db['scenario'] = zip(*db['scenario'].apply(lambda x: x.split('|', 1)))

        colors = {scen: utils.get_color(scen) for scen in db['scenario'].unique()}
        fig = create_scatter_plot(db, colors, model, year)

    return fig

def process_dispatch_data(min_days, max_days):
    """Process Min and Max Dispatch data to create DataFrames for table rendering."""
    min_date = pd.DataFrame(
        {'scenario': min_day['scenario'], 'variable': 'Min Dispatch Day', 'value': min_day['date']} 
        for _, min_day in min_days.iterrows()
    )
    max_date = pd.DataFrame(
        {'scenario': max_day['scenario'], 'variable': 'Max Dispatch Day', 'value': max_day['date']} 
        for _, max_day in max_days.iterrows()
    )
    min_dispatch = pd.DataFrame(
        {'scenario': min_day['scenario'], 'variable': 'Min Dispatch Value', 'value': min_day['value']} 
        for _, min_day in min_days.iterrows()
    )
    max_dispatch = pd.DataFrame(
        {'scenario': max_day['scenario'], 'variable': 'Max Dispatch Value', 'value': max_day['value']} 
        for _, max_day in max_days.iterrows()
    )

    # Group and aggregate the data
    min_date = min_date.groupby(['scenario', 'variable'])['value'].apply(lambda x: ', '.join(x)).reset_index()
    max_date = max_date.groupby(['scenario', 'variable'])['value'].apply(lambda x: ', '.join(x)).reset_index()
    min_dispatch = min_dispatch.groupby(['scenario', 'variable'])['value'].first().reset_index()
    max_dispatch = max_dispatch.groupby(['scenario', 'variable'])['value'].first().reset_index()

    return min_date, max_date, min_dispatch, max_dispatch

def create_plotly_table(df_pivot, values):
    """Create a Plotly table figure from the pivoted DataFrame."""
    header_values = [''] + list(df_pivot.columns)
    cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

    min_value = values.apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
    max_value = values.apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

    def normalize(value):
        return (value - min_value) / (max_value - min_value) if isinstance(value, (int, float)) else None

    colors = [np.array([px.colors.sample_colorscale('Blues', normalize(val))[0] if normalize(val) is not None else 'rgb(255,255,255)' for val in df_pivot[col]]) for col in df_pivot.columns]
    colors_by_row = [['#ffffff', '#e5eeec'] * (len(df_pivot.index) // 2)] + colors
    font_colors = [['#000000'] * len(df_pivot.index)] + [[get_contrasting_font_color(color) for color in column] for column in colors]

    column_width = [max(df_pivot.index.str.len()) * 8] + [max([len(str(col))] + [len(str(val)) for val in df_pivot[col]]) * 8 for col in df_pivot.columns]

    return go.Figure(data=[go.Table(
        columnorder=[i + 1 for i in range(len(df_pivot.columns) + 1)],
        columnwidth=column_width,
        header=dict(values=header_values, fill_color=['#ffffff', '#248ce6', '#248ce6'], font=dict(color='white'), align='center'),
        cells=dict(values=cell_values, fill_color=colors_by_row, line_color=colors_by_row, font=dict(color=font_colors), align='left')
    )])

def create_scatter_plot(db, colors, model, year):
    """Create a scatter plot figure from the DataFrame."""
    fig = go.Figure()

    def add_scatter_trace(data, name, color, is_comparison):
        fig.add_trace(go.Scatter(x=data['variable'], y=data['value'], mode='markers', name=name, marker=dict(color=color, size=10),
                                    text=data['m_scen'] if is_comparison else data['scenario'],
                                    hovertemplate='<b>%{text}</b><br><br>' +
                                                  'Variable: %{x}<br>' +
                                                  'Value: %{y}<extra></extra>',


                                 ))

    for scenario in db['scenario'].unique():
        scenario_data = db[db['scenario'] == scenario]
        color = colors[scenario]
        add_scatter_trace(scenario_data, scenario, color, model=='Generic Comparison')

    fig.update_layout(
        xaxis_title='Variable',
        yaxis_title='Value',
        title=f'Output Stats for {model} in {year}',
        template="simple_white"
    )
    fig.update_layout(scattermode="group", scattergap=0.75)
    return fig


def create_plot(model, is_comparison=False):
    def plot(df, window_id):
        '''

        :param df: pandas Dataframe containing the data to visualize
        :param window_id: window id to use when registering components to dash
        :return: html.Div([widgets]), dcc.Graph(plot)
        '''
        years = df['time'].unique().tolist()
        # sort years
        years.sort()
        scenarios = df['scenario'].unique().tolist()

        comparison_widgets = []
        if is_comparison:
            base_scenarios = df['base_scenario'].unique().tolist()
            base_scenarios = ['ALL'] + base_scenarios

            comparison_widgets = [
                dmc.Select(
                    label='Scenario Group',
                    data=[{'label': scenario, 'value': scenario} for scenario in base_scenarios],
                    value='ALL',
                    id={
                        'type': 'scenario-group-select',
                        'model': model,
                        'index': window_id,
                        'viz': 'output_stats'
                    },
                    style={'display': 'block'}
                ),
            ]

        widget_layout = html.Div([
            dmc.Select(
                label='Plot Type',
                data=[{'label': p_type, 'value': p_type} for p_type in ['Table', 'Scatter']],
                value='Table',
                id={
                    'type': 'plot-select',
                    'index': window_id,
                    'model': model,
                    'viz': 'output_stats'
                },
            ),

            *comparison_widgets,

            dmc.Select(
                label='Year',
                data=[{'label': year, 'value': year} for year in years],
                value=years[0],
                id={
                    'type': 'year-select',
                    'index': window_id,
                    'model': model,
                    'viz': 'output_stats'
                },
            ),
            dmc.MultiSelect(
                label='Scenario',
                value=[''],
                data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                id={
                    'type': 'scenario-select',
                    'index': window_id,
                    'model': model,
                    'viz': 'output_stats'
                },
            ),
            dmc.Button('Download Data', id={'type': 'download-button', 'index': window_id, 'model': model,
                                            'viz': 'output_stats'},
                       variant='light',
                       # center the button
                       style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
            dcc.Download(id={'type': 'download', 'index': window_id, 'model': model,
                             'viz': 'output_stats'}),
        ])

        df = df[df.scenario.isin([''])]

        plot_layout = dcc.Graph(
            figure=render_plot('Table', df, years[0], model),
            id={
                'type': ids.FIGURE,
                'index': window_id,
                'model': model,
                'viz': 'output_stats'
            },
            style={
                'width': '100%',
                'height': '100%'
            }

        )

        return widget_layout, plot_layout

    return plot
