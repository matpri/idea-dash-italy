import pandas as pd
from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):


    demand_scenarios = []
    demand_years = []
    demand_months = []
    demand_dates = []
    if 'Demand' in classes:
        demand = df[df['variable'].str.startswith('Demand')].copy()
        demand['time'] = pd.to_datetime(demand['time'])
        demand_scenarios = demand['scenario'].unique()
        demand_years = demand['time'].dt.year.unique()
        demand_months = demand['time'].dt.strftime('%B').unique()
        demand_dates = demand['time'].dt.strftime('%d').unique()

    demand_widget_layout = html.Div([
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in demand_scenarios],
            value=demand_scenarios[0] if len(demand_scenarios) else '',
            id={
                'type': 'copper-inputs-demand-scenario-select',
                'index': window_id,
            },
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