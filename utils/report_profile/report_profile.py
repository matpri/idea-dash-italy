from random import randint

import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

class ReportProfile:
    def __init__(self, name, report, descriptions=None):
        self.display_name = name
        self.name = name
        self.color = '#000000'
        self.description = 'Report Profile'
        self.viz_options = {}
        self.plot_order = ['Report']

        self.descriptions = descriptions if descriptions is not None else {}

        def show_report(_x, _window_id):
            return None, dcc.Markdown(report,
                                      id={
                                          'type': 'markdown',
                                          'index': _window_id,
                                          'profile': name
                                      }
                                      )

        self.viz_options['Report'] = {
            'check': lambda x: True,
            'db_check': lambda x: True,
            'process': lambda x: x,
            'db_process': lambda x: x,
            'viz': show_report,
        }
