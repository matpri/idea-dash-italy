import dash
import dash_lumino_components as dlc
from dash import html
from components import ids

def render(app):
    layout = dlc.DockPanel([
        ], id=ids.PLOT_CANVAS)
    return layout