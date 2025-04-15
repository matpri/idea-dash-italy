from dash import html, dcc

from components import ids
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

    if type(plot) == dcc.Markdown:
        _md = html.Div(plot, id={'index': card_id, 'type': 'MD'}, style={
            'width': '100%',
            'height': '100%',
            'overflow': 'auto'
        }
                       )
        _f = dcc.Graph(
            figure={},
            id={'type': ids.PLOT, 'index': card_id},
            style={
                'width': '0%',
                'height': '0%',
                'display': 'none'
            }
        )
    else:
        _md = html.Div([], id={'index': card_id, 'type': 'MD'}, style={
            'width': '0%',
            'height': '0%',
            'overflow': 'auto',
            'display': 'none'
        }
                       )

        _f = dcc.Graph(figure=plot.figure, id={'type': ids.PLOT, 'index': card_id},
                       style={
                           'width': '100%',
                           'height': '100%'
                       }
                       )

    return (*drawer.render(card_id, widgets),
            _f,
            _md,
            html.Div(plot if type(plot) != dcc.Markdown else [],
                     id={
                         'type': 'hidden_plot',
                         'index': card_id
                     },
                     style={'display': 'none'})
            )
