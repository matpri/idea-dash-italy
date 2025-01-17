import dash
from dash import html, Input, Output, State, MATCH, no_update, dcc
from components import ids
import plotly.io as pio


def link(app):
    '''
    This callback is used to start the export functionality for figures.
    For now this is simply downloading the current figure as a png file. In the Future this could include a full screen view of the figure.
    :param app:
    :return:
    '''

    @app.callback(
        Output({'type': 'fig-download', 'index': MATCH}, 'data'),
        Input({'type': 'export-tab', 'index': MATCH}, 'n_clicks'),
        State({'type': ids.PLOT_POPUP_GRAPH, 'index': MATCH}, 'figure'),
        State({'type': ids.PLOT_POPUP_WIDTH, 'index': MATCH}, 'value'),
        State({'type': ids.PLOT_POPUP_HEIGHT, 'index': MATCH}, 'value'),

        prevent_initial_call=True,
    )
    def export_fig(n_clicks, figure, width, height):
        '''
        This function is used to download the current figure as a png file.
        :param n_clicks: The number of times the export button has been clicked
        :param figure: The current figure to be exported
        :return: The data for the download component
        '''
        if n_clicks is None:
            return no_update
        print('downloading graph', n_clicks)
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if 'export-tab' not in triggered_id:
            return no_update

        png_data = pio.to_image(figure, format="png", engine='kaleido',
                                width=width, height=height)
        # Return the image for download
        return dcc.send_bytes(png_data, "figure.png")
