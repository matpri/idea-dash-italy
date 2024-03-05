from dash import html
import dash_lumino_components

from components.plot_window import drawer


def render(card_id, profile, viz, widgets, plot):
    print('rendering viz container', card_id, profile, viz)

    return drawer.render(card_id, widgets), html.Div(plot, id={'type': 'plot', 'index': card_id})
