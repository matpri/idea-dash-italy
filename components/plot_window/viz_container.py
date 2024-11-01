from dash import html, dcc
from components.plot_window import drawer

def render(card_id, profile, viz, widgets, plot):
    """
    Render the visualization container with the specified parameters.

    Parameters:
    - card_id: Unique identifier for the card.
    - profile: Profile associated with the visualization.
    - viz: Visualization type.
    - widgets: Widgets to be displayed alongside the plot.
    - plot: Plot data to be rendered.

    Returns:
    - A tuple containing the rendered drawer and the plot.
    """
    print('rendering viz container', card_id, profile, viz)

    return (*drawer.render(card_id, widgets),
            dcc.Graph(figure=plot.figure, id={'type': 'plot', 'index': card_id},
                      style={
                          'width': '100%',
                          'height': '100%'
                      }
                      ),
            html.Div(plot,
                     id={
                         'type': 'hidden_plot',
                         'index': card_id
                     },
                     style={'display': 'none'})
            )
