import base64
import io
from functools import partial
from typing import List, Dict

import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html, Output, Input, State
from dash_iconify import DashIconify

from components import ids
from components.data_selection import viz_edit_modal


def render():
    layout = dmc.AccordionItem([
        dmc.AccordionControl('Local Files:'),
        dmc.AccordionPanel('Upload Local Results file', id=ids.DATA_SELECTED)
    ],
        value='local',
        style={'width': '100%'})


    return layout




