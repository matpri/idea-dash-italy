import dash
from dash import Output, Input, State, MATCH, dcc

from profiles.recap.visualization_scripts.stock_lcc import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'recap',
            'viz': 'Overview'
        }, 'figure', allow_duplicate=True),
        Output({
            'type': 'recap-stock_lcc-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-stock_lcc-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-stock_lcc-service-select',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'recap-stock_lcc-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'recap-stock_lcc-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-stock_lcc-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output(
            {
                'type': 'recap-stock_lcc-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'recap-stock_lcc-text-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'recap-stock_lcc-service-select',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'recap-stock_lcc-sector-select',
                'index': MATCH
            },
            'style'
        ),
        Input({
            'type': 'recap-stocks-update',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-representation-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-variable-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-year-select',
            'index': MATCH
        }, 'value'),
        Input(
            {
                'type': 'recap-stock_lcc-pattern-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'recap-stock_lcc-text-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'recap-stock_lcc-download-button',
            'index': MATCH
        }, 'n_clicks'),
        Input({
            'type': 'recap-stock_lcc-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-stock_lcc-service-select',
            'index': MATCH
        }, 'value'),
        State({
            'type': 'recap-stock_lcc-region-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'recap-stock_lcc-year-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'recap',
            'viz': 'Overview'
        }, 'figure'),
        State({
            'type': 'recap-stock_lcc-download',
            'index': MATCH
        }, 'data'),
        State({
            'type': 'recap-stock_lcc-scenario-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'recap-stock_lcc-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        State(
            {
                'type': 'recap-stock_lcc-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'recap-stock_lcc-text-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'recap-stock_lcc-service-select',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'recap-stock_lcc-sector-select',
                'index': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_stock_lcc(_update, _rep, _p_type, _scenarios, _scenario, _variable, _regions, _years, _pattern, _text,
                         _download, _sector, _service, _r_style, _y_style, _canvas, _data, _s_style, _m_style,
                         _pattern_style, _text_style, _service_style, _sector_style):
        print('updating stock_lcc plot', _variable)
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        _data = data_handler.processed_data['recap']['Overview']
        _data = _data[_data['tab'] == 'Technology Stocks']

        if 'recap-stock_lcc-download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(_data.to_csv,
                                        "stock_lcc.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _pattern_style, _text_style, _service_style, _sector_style

        if _rep == 'By Sector':
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'none'}
        else:
            _sector_style = {'display': 'block'}
            _service_style = {'display': 'block'}


        services = dash.no_update
        if 'recap-stock_lcc-sector-select' in trigger_id['type']:
            _data = _data[_data['sector'] == _sector]
            services = _data[_data['technology'].isna()]['short_path'].unique().tolist()

        if _p_type == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot('By Year',
                                  _data,
                                  _rep,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector, service=_service,
                                  parameter=_variable, plot_name=_variable)

        elif _p_type == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot('Trend Over Years',
                                  _data,
                                  _rep,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector, service=_service,
                                  parameter=_variable, plot_name=_variable)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot('Pie Chart',
                                  _data,
                                  _rep,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector, service=_service,
                                  parameter=_variable, plot_name=_variable)

        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot('By Region',
                                  _data,
                                  _rep,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector, service=_service,
                                  parameter=_variable, plot_name=_variable)

        return _canvas, _r_style, _y_style, services, dash.no_update, _s_style, _m_style, _pattern_style, _text_style, _service_style, _sector_style
