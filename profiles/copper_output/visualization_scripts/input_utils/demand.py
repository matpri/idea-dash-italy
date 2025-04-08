import pandas as pd
from dash import html
import dash_mantine_components as dmc
import plotly.graph_objects as go

from profiles.copper_output import utils


def create_widgets(df, classes, window_id):


    demand_scenarios = []
    demand_years = []
    demand_months = []
    demand_dates = []
    regions = []
    if 'Demand' in classes:
        demand = df[df['variable'].str.startswith('Demand')].copy()
        demand['time'] = pd.to_datetime(demand['time'])
        demand_scenarios = demand['scenario'].unique()
        demand_years = demand['time'].dt.year.unique()
        demand_months = demand['time'].dt.strftime('%B').unique()
        demand_dates = demand['time'].dt.strftime('%d').unique()

        regions = ['Total'] + demand['region'].unique().tolist()

    demand_widget_layout = html.Div([
        dmc.Select(
          label = 'Plot Type',
            data=[{'label': cls, 'value': cls} for cls in ['By Scenario', 'By Region']],
            value='By Scenario',
            id={
                'type': 'copper-inputs-demand-plot-type-select',
                'index': window_id,
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in demand_scenarios],
            value=demand_scenarios[0] if len(demand_scenarios) else '',
            id={
                'type': 'copper-inputs-demand-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in demand_scenarios],
            value=[demand_scenarios[0]] if len(demand_scenarios) else [],
            id={
                'type': 'copper-inputs-demand-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
          label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value=regions[0] if len(regions) else '',
            id={
                'type': 'copper-inputs-demand-region-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value='yearly',
            id={
                'type': 'copper-inputs-demand-time_step-select',
                'index': window_id,
            },
        ),
        dmc.Select(
          label='Year',
            data=[{'label': year, 'value': year} for year in demand_years],
            value=demand_years[0] if len(demand_years) else '',
            id={
                'type': 'copper-inputs-demand-year-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Month',
            data=[{'label': month, 'value': month} for month in demand_months],
            value=demand_months[0] if len(demand_months) else '',
            id={
                'type': 'copper-inputs-demand-month-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Date',
            data=[{'label': date, 'value': date} for date in demand_dates],
            value=demand_dates[0] if len(demand_dates) else '',
            id={
                'type': 'copper-inputs-demand-date-select',
                'index': window_id,
            },
            style={'display': 'none'}
        )
        ],
        id={
            'type': 'copper-inputs-demand-widget',
            'index': window_id
        },
        style={'display': 'none'},)
    return demand_widget_layout

def render(plot_type, df, scenario, multi_scenario, region, year, month, date, title, x_axis_label, y_axis_label, time_size='hourly'):
    # turn date range into a readable format

    fig = go.Figure()
    # add title
    fig.update_layout(
        title_text=title + ' - ' + plot_type,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )
    df_scen = df.copy(deep=True)

    if region == 'Total' and plot_type == 'By Scenario':
        df_scen['region'] = 'Total'

    df_scen = df_scen[df_scen['scenario'] == scenario] if plot_type == 'By Region' else df_scen[df_scen['scenario'].isin(multi_scenario) & (df_scen['region'] == region)]


    df_scen['time'] = pd.to_datetime(df_scen['time'])
    # groupby time based on time_size
    if time_size == 'daily':
        df_scen = df_scen[df_scen['time'].dt.year == year]
        df_scen = df_scen[df_scen['time'].dt.strftime('%B') == month]
        df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m-%d')
    elif time_size == 'monthly':
        df_scen = df_scen[df_scen['time'].dt.year == year]
        df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m')
    elif time_size == 'yearly':
        df_scen['time'] = df_scen['time'].dt.strftime('%Y')
    else:
        df_scen = df_scen[df_scen['time'].dt.year == year]
        df_scen = df_scen[df_scen['time'].dt.strftime('%B') == month]
        df_scen = df_scen[df_scen['time'].dt.strftime('%d') == date]
        df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    cols = df_scen.columns.tolist()
    # remove value column
    cols.remove('value')
    df_scen = df_scen.groupby(['time', 'region']).sum(numeric_only=True).reset_index() if plot_type == 'By Region' else df_scen.groupby(['time', 'scenario']).sum(numeric_only=True).reset_index()

    variables = df_scen.region.unique().tolist() if plot_type == 'By Region' else df_scen.scenario.unique().tolist()


    # Create a stacked area chart (original behavior)
    for var in variables:
        df_tech = df_scen[df_scen['region'] == var] if plot_type == 'By Region' else df_scen[df_scen['scenario'] == var]
        df_tech = df_tech.sort_values(by=['time'])
        fig.add_trace(go.Scatter(
            x=df_tech['time'],
            y=df_tech['value'],
            name=var,
            mode='lines',
            line=dict(color=utils.get_color(var)) if plot_type == 'By Region' else dict(color=utils.get_color(scenario)),
            stackgroup='one' if plot_type == 'By Region' else '',
            hovertemplate=f'<b>{var}</b><br><br>' +
                          'Time: %{x}<br>' +
                          f'Demand: %{{y:.2f}} {y_axis_label}<br>' +
                          '<extra></extra>'
        ))
    fig.update_yaxes(showgrid=True)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.layout.autosize = True
    return fig