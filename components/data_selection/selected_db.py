import base64
import io
from functools import partial
from typing import List, Dict

import dash_mantine_components as dmc
import pandas as pd
from dash_iconify import DashIconify
from dash import html, Output, Input, State

from components import ids
from components.data_selection import viz_edit_modal

def render():
    from main import app
    layout = html.Div([
                    dmc.Text('Database:'),], id=ids.DB_SELECTED)
    return layout

