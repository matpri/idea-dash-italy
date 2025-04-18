import dash
from dash import Output, Input, State, MATCH, dcc

from profiles.cims_output.visualization_scripts.ghg import render_plot
from components import ids

emissions_mapping = {
    'Net Emissions': ['total_cumul_net_emissions'],
    'Avoided Emissions': ['total_cumul_avoided_emissions'],
    'Negative Emissions': ['total_cumul_negative_emissions'],
    'Emitted Emissions': ['total_cumul_net_emissions', 'total_cumul_bio_emissions'],
    'Emissions Costs': ['total_cumul_emissions_cost']}


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'CIMS',
            'viz': 'Overview'
        }, 'figure', allow_duplicate=True),
        Output({
            'type': 'cims-ghg-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-ghg-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-ghg-service-widgets',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-ghg-service-select',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-ghg-service-select',
            'index': MATCH
        }, 'value'),
        Output({
            'type': 'cims-ghg-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-ghg-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-ghg-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output(
            {
                'type': 'cims-ghg-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'cims-ghg-text-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'cims-ghg-sector-select',
                'index': MATCH
            },
            'style'
        ),
        Input({
            'type': 'cims-emissions-update',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-representation-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-year-select',
            'index': MATCH
        }, 'value'),
        Input(
            {
                'type': 'cims-ghg-pattern-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'cims-ghg-text-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'cims-ghg-download-button',
            'index': MATCH
        }, 'n_clicks'),
        Input({
            'type': 'cims-ghg-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-service-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-service-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-ghg-emission-select',
            'index': MATCH
        }, 'value'),
        State({
            'type': 'cims-ghg-region-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-ghg-year-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'CIMS',
            'viz': 'Overview'
        }, 'figure'),
        State({
            'type': 'cims-ghg-download',
            'index': MATCH
        }, 'data'),
        State({
            'type': 'cims-ghg-scenario-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-ghg-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        State(
            {
                'type': 'cims-ghg-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'cims-ghg-text-switch',
                'index': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_ghg(_update, _representation, _p_type, _scenarios, _scenario, _regions, _years, _pattern, _text,
                   _download, _sector, _service_sector, _service, _emission, _r_style, _y_style, _canvas, _data, _s_style, _m_style,
                   _pattern_style, _text_style):
        # print('updating ghg plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        _data = data_handler.processed_data['CIMS']['Overview']
        _data = _data[_data['tab'] == 'Emissions']
        services = dash.no_update
        _service_style = dash.no_update

        if 'cims-ghg-download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(_data.to_csv, "ghg.csv")
            return _canvas, _r_style, _y_style, _service_style, _service, services,  _data, _s_style, _m_style, _pattern_style, _text_style, dash.no_update


        emissions_list = _data[_data['parameter'].str.contains('emissions')]['parameter'].unique().tolist()
        to_use = emissions_mapping[_emission]
        emissions_list = [e_type for e_type in emissions_list if e_type in to_use]

        if 'cims-ghg-service-sector-select' in trigger_id['type']:
            _data = _data[_data['sector'] == _service_sector]
            services = _data[_data.parameter.isin(emissions_list)]['short_path'].unique().tolist()
            _service = services[0]

        if _representation == 'By Emission':
            _sector_style = {'display': 'block'}
            _service_style = {'display': 'none'}

        elif _representation == 'By Service':
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'block'}
        else:
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'none'}

        if _p_type == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation, 'By Year', _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector if _representation == 'By Emission' else _service_sector, service=_service,
                                  emissions_list=emissions_list, plot_name=_emission)

        elif _p_type == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Trend Over Years',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector if _representation == 'By Emission' else _service_sector, service=_service,
                                  emissions_list=emissions_list, plot_name=_emission)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Pie Chart', _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector if _representation == 'By Emission' else _service_sector, service=_service,
                                  emissions_list=emissions_list, plot_name=_emission)

        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation, 'By Region', _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector if _representation == 'By Emission' else _service_sector,
                                  service=_service,
                                  emissions_list=emissions_list, plot_name=_emission)

        return _canvas, _r_style, _y_style, _service_style,services, _service, dash.no_update, _s_style, _m_style, _pattern_style, _text_style, _sector_style
