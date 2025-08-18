import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
from profiles.recap.visualization_scripts.utils import bar_over_years, trend_over_years


def render_credits_by_sector(plot_type, df, scenarios, region, scenario, credit_type='Credit Supply'):
    """
    Render credits by sector visualization
    
    Args:
        plot_type: 'By Year' or 'Trend Over Years'
        df: DataFrame with credits data
        scenarios: List of scenarios for 'By Year' plots
        region: Selected region
        scenario: Selected scenario for 'Trend Over Years'
        credit_type: Type of credits to display (Credit Supply, Credit Demand, Net Balance)
    """
    # Filter data for the selected credit type
    filtered_df = df[df['credit_type'] == credit_type].copy()
    
    if filtered_df.empty:
        # Return empty plot if no data
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text=f"No data available for {credit_type}",
            showarrow=False,
            xref="paper", yref="paper",
            font=dict(size=16)
        )
        fig.update_layout(
            title=f"Credits by Sector - {credit_type}",
            template="simple_white"
        )
        return fig
    
    # Rename display_variable to variable for compatibility with existing plotting functions
    filtered_df = filtered_df.rename(columns={'display_variable': 'variable'})
    
    # Get unit from data
    unit = filtered_df['unit'].iloc[0] if not filtered_df.empty else 'Credits'
    
    if plot_type == 'By Year':
        return bar_over_years.plot(
            df=filtered_df,
            scenarios=scenarios,
            region=region,
            title=f"Credits by Sector - {credit_type} (By Year)",
            x_axis_label="Year",
            y_axis_label=f"{credit_type} ({unit})",
            tooltip_name=credit_type,
            unit=unit,
            aggregate=False,
            pattern_active=True,
            text_active=False
        )
    elif plot_type == 'Trend Over Years':
        return trend_over_years.plot(
            df=filtered_df,
            scenario=scenario,
            region=region,
            aggregate=False,
            title=f"Credits by Sector - {credit_type} (Trend)",
            x_axis_label="Year",
            y_axis_label=f"{credit_type} ({unit})",
            tooltip_name=credit_type,
            unit=unit
        )


def plot(df, window_id):
    """
    Create the widget layout and plot for credits visualization
    
    Args:
        df: DataFrame containing credits data
        window_id: Unique identifier for this widget instance
    
    Returns:
        tuple: (widget_layout, plot_layout)
    """
    if df.empty:
        # Handle empty data case
        widget_layout = html.Div([
            dmc.Alert(
                "No credits data available. Please ensure your data contains variables starting with 'Credits|'",
                title="No Credits Data",
                color="yellow"
            )
        ])
        
        plot_layout = dcc.Graph(
            figure={
                'data': [],
                'layout': {
                    'title': 'No Credits Data Available',
                    'template': 'simple_white'
                }
            },
            id={
                'type': ids.FIGURE,
                'index': window_id,
                'profile': 'Summary',
                'viz': 'Economy-wide Carbon Credits'
            }
        )
        
        return widget_layout, plot_layout
    
    # Extract unique values for dropdowns
    scenarios = sorted(df['scenario'].unique().tolist())
    regions = sorted(df['region'].unique().tolist())
    credit_types = sorted(df['credit_type'].unique().tolist())
    
    # Create widget layout
    widget_layout = html.Div([
        dmc.Select(
            label='Plot Type',
            data=[
                {'label': 'By Year', 'value': 'By Year'},
                {'label': 'Trend Over Years', 'value': 'Trend Over Years'}
            ],
            value='By Year',
            id={
                'type': 'recap-credits-plot-type',
                'index': window_id
            }
        ),
        
        dmc.Select(
            label='Credit Type',
            data=[{'label': ct, 'value': ct} for ct in credit_types],
            value=credit_types[0] if credit_types else 'Credit Supply',
            id={
                'type': 'recap-credits-type',
                'index': window_id
            }
        ),
        
        # Widgets for "By Year" plot type
        html.Div([
            dmc.MultiSelect(
                label='Scenarios',
                data=[{'label': s, 'value': s} for s in scenarios],
                value=[scenarios[0]] if scenarios else [],
                id={
                    'type': 'recap-credits-scenarios-multi',
                    'index': window_id
                }
            ),
            dmc.Select(
                label='Region',
                data=[{'label': r, 'value': r} for r in regions],
                value=regions[0] if regions else None,
                id={
                    'type': 'recap-credits-region',
                    'index': window_id
                }
            )
        ], id={
            'type': 'recap-credits-by-year-widgets',
            'index': window_id
        }),
        
        # Widgets for "Trend Over Years" plot type
        html.Div([
            dmc.Select(
                label='Scenario',
                data=[{'label': s, 'value': s} for s in scenarios],
                value=scenarios[0] if scenarios else None,
                id={
                    'type': 'recap-credits-scenario',
                    'index': window_id
                }
            ),
            dmc.Select(
                label='Region',
                data=[{'label': r, 'value': r} for r in regions],
                value=regions[0] if regions else None,
                id={
                    'type': 'recap-credits-region-trend',
                    'index': window_id
                }
            )
        ], 
        style={'display': 'none'},
        id={
            'type': 'recap-credits-trend-widgets',
            'index': window_id
        }),
        
        dmc.Button(
            'Download Data',
            id={
                'type': 'recap-credits-download-button',
                'index': window_id
            },
            variant='light',
            style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}
        ),
        
        dcc.Download(id={
            'type': 'recap-credits-download',
            'index': window_id
        })
    ])
    
    # Create initial plot
    initial_credit_type = credit_types[0] if credit_types else 'Credit Supply'
    initial_scenarios = [scenarios[0]] if scenarios else []
    initial_region = regions[0] if regions else None
    
    plot_layout = dcc.Graph(
        figure=render_credits_by_sector(
            plot_type='By Year',
            df=df,
            scenarios=initial_scenarios,
            region=initial_region,
            scenario=scenarios[0] if scenarios else None,
            credit_type=initial_credit_type
        ),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'Summary',
            'viz': 'Economy-wide Carbon Credits'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    
    return widget_layout, plot_layout