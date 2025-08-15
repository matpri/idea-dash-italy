import dash
from dash import Output, Input, State, MATCH, dcc
from profiles.recap.visualization_scripts.credits import render_credits_by_sector
from components import ids


def link(app):
    @app.callback(
        Output({'type': ids.FIGURE, 'index': MATCH, 'profile': 'Summary', 'viz': 'Credits'}, 'figure'),
        Output({'type': 'recap-credits-download', 'index': MATCH}, 'data'),
        Output({'type': 'recap-credits-by-year-widgets', 'index': MATCH}, 'style'),
        Output({'type': 'recap-credits-trend-widgets', 'index': MATCH}, 'style'),
        
        # Inputs
        Input({'type': 'recap-credits-plot-type', 'index': MATCH}, 'value'),
        Input({'type': 'recap-credits-type', 'index': MATCH}, 'value'),
        
        # By Year inputs
        Input({'type': 'recap-credits-scenarios-multi', 'index': MATCH}, 'value'),
        Input({'type': 'recap-credits-region', 'index': MATCH}, 'value'),
        
        # Trend inputs
        Input({'type': 'recap-credits-scenario', 'index': MATCH}, 'value'),
        Input({'type': 'recap-credits-region-trend', 'index': MATCH}, 'value'),
        
        # Download button
        Input({'type': 'recap-credits-download-button', 'index': MATCH}, 'n_clicks'),
        
        # States
        State({'type': ids.FIGURE, 'index': MATCH, 'profile': 'Summary', 'viz': 'Credits'}, 'figure'),
        State({'type': 'recap-credits-download', 'index': MATCH}, 'data'),
        State({'type': 'recap-credits-by-year-widgets', 'index': MATCH}, 'style'),
        State({'type': 'recap-credits-trend-widgets', 'index': MATCH}, 'style'),
        
        prevent_initial_call=True
    )
    def update_credits_plot(
        plot_type, credit_type,
        scenarios_multi, region_by_year,
        scenario_trend, region_trend,
        download_clicks,
        figure, download_data, by_year_style, trend_style
    ):
        """
        Update credits visualization based on user inputs
        """
        from utils.data_state import data_handler
        
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        
        # Handle download button click
        if 'recap-credits-download-button' in trigger_id['type']:
            download_data = dcc.send_data_frame(
                data_handler.processed_data['Summary']['Credits'].to_csv,
                "credits.csv"
            )
            return (
                dash.no_update, download_data, dash.no_update, dash.no_update
            )
        
        # Get the data
        credits_data = data_handler.processed_data['Summary']['Credits']
        
        # Update widget visibility based on plot type
        if plot_type == 'By Year':
            by_year_style = {'display': 'block'}
            trend_style = {'display': 'none'}
        else:  # Trend Over Years
            by_year_style = {'display': 'none'}
            trend_style = {'display': 'block'}
        
        # Get parameters for rendering
        if plot_type == 'By Year':
            scenarios = scenarios_multi if scenarios_multi else []
            region = region_by_year
            scenario = scenarios[0] if scenarios else None
        else:  # Trend Over Years
            scenarios = []
            scenario = scenario_trend
            region = region_trend
        
        # Render the plot
        figure = render_credits_by_sector(
            plot_type=plot_type,
            df=credits_data,
            scenarios=scenarios,
            region=region,
            scenario=scenario,
            credit_type=credit_type if credit_type else 'Credit Supply'
        )
        
        return (
            figure,
            dash.no_update,
            by_year_style,
            trend_style
        )