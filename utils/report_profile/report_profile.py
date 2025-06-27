from random import randint

import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

class ReportProfile:
    def __init__(self, name, reports, descriptions=None):
        self.display_name = name
        self.name = name
        self.color = '#000000'
        self.description = 'Report Profile'
        self.viz_options = {}
        self.plot_order = [r for r in reports.keys()]

        self.descriptions = descriptions if descriptions is not None else {}

        def show_report(md_report):
            def show(_x, _window_id):
                return None, dcc.Markdown(md_report,
                                          id={
                                              'type': 'markdown',
                                              'index': _window_id,
                                              'profile': name
                                          }
                                          )
            return show

        for report_name, report in reports.items():
            self.viz_options[report_name] = {
                'check': lambda x: True,
                'db_check': lambda x: True,
                'process': lambda x: x,
                'db_process': lambda x: x,
                'viz': show_report(report)
            }
