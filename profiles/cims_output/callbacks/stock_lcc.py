import dash
from dash import Output, Input, State, MATCH, dcc

from profiles.cims_output.visualization_scripts.stock_lcc import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'stock_lcc'
        }, 'figure'),
        Output({
            'type': 'cims-stock_lcc-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-stock_lcc-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-stock_lcc-service-select',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-stock_lcc-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-stock_lcc-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-stock_lcc-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output(
            {
                'type': 'cims-stock_lcc-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'cims-stock_lcc-text-switch',
                'index': MATCH
            },
            'style'
        ),
        Input({
            'type': 'cims-stock_lcc-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-stock_lcc-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-stock_lcc-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-stock_lcc-variable-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-stock_lcc-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-stock_lcc-year-select',
            'index': MATCH
        }, 'value'),
        Input(
            {
                'type': 'cims-stock_lcc-pattern-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'cims-stock_lcc-text-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'cims-stock_lcc-download-button',
            'index': MATCH
        }, 'n_clicks'),
        Input({
            'type': 'cims-stock_lcc-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-stock_lcc-service-select',
            'index': MATCH
        }, 'value'),
        State({
            'type': 'cims-stock_lcc-region-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-stock_lcc-year-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'stock_lcc'
        }, 'figure'),
        State({
            'type': 'cims-stock_lcc-download',
            'index': MATCH
        }, 'data'),
        State({
            'type': 'cims-stock_lcc-scenario-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-stock_lcc-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        State(
            {
                'type': 'cims-stock_lcc-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'cims-stock_lcc-text-switch',
                'index': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_stock_lcc(_p_type, _scenarios, _scenario, _variable, _regions, _years, _pattern, _text,
                         _download, _sector, _service, _r_style, _y_style, _canvas, _data, _s_style, _m_style,
                         _pattern_style, _text_style):
        print('updating stock_lcc plot', _variable)
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'cims-stock_lcc-download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(data_handler.processed_data['CIMS']['Technology Stocks'].to_csv,
                                        "stock_lcc.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _pattern_style, _text_style

        services = dash.no_update
        if 'cims-stock_lcc-sector-select' in trigger_id['type']:
            _data = data_handler.processed_data['CIMS']['Technology Stocks']
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
                                  data_handler.processed_data['CIMS']['Technology Stocks'],
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
                                  data_handler.processed_data['CIMS']['Technology Stocks'],
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
                                  data_handler.processed_data['CIMS']['Technology Stocks'],
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
                                  data_handler.processed_data['CIMS']['Technology Stocks'],
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector, service=_service,
                                  parameter=_variable, plot_name=_variable)

        return _canvas, _r_style, _y_style, services, dash.no_update, _s_style, _m_style, _pattern_style, _text_style
