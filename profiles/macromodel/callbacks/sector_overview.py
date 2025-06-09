import dash
from dash import Output, Input, State, MATCH, dcc, MATCH

from components import ids
from profiles.macromodel.visualization_scripts import sector_overview

render_func = {
    'sector_overview': sector_overview.render_plot
}

def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile':MATCH,
            'name': MATCH
        }, 'figure', allow_duplicate=True),
        Output({
            'type': 'so-region-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-year-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-download',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        Output({
            'type': 'so-scenario-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-scenario-multi-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-unit-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output({
            'type': 'so-vartype-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        Output(
            {
                'type': 'so-pattern-switch',
                'index': MATCH,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'so-text-switch',
                'index': MATCH,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        Input({
            'type': 'so-plot-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-aggregate-switch',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'checked'),
        Input({
            'type': 'so-scenario-multi-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-scenario-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-region-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-year-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-unit-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input({
            'type': 'so-vartype-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'value'),
        Input(
            {
                'type': 'so-pattern-switch',
                'index': MATCH,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'so-text-switch',
                'index': MATCH,
                'profile': MATCH,
                'name': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'so-download-button',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'n_clicks'),
        State({
            'type': 'so-region-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-year-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'figure'),
        State({
            'type': 'so-download',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'data'),
        State({
            'type': 'so-scenario-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-scenario-multi-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-unit-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State({
            'type': 'so-vartype-select',
            'index': MATCH,
            'profile': MATCH,
            'name': MATCH
        }, 'style'),
        State(
            {
                'type': 'so-pattern-switch',
                'index': MATCH,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'so-text-switch',
                'index': MATCH,
                'profile': MATCH,
                'name': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _units, _vartypes, _pattern, _text,
                           _download, _r_style, _y_style, _canvas, _data, _s_style, _m_style, _u_style, _v_style, _pattern_style,
                           _text_style):
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = 'Macromodel'
        name = trigger_id['name']
        print(f'updating sector_overview {name}, {model} plot')
        render_plot = render_func[trigger_id['name']]

        if 'download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _r_style, _y_style,_data, _s_style, _m_style, _u_style, _v_style, _pattern_style, _text_style



        print('plot type:', _p_type)
        if _p_type == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _u_style = {'display': 'block'}
            _v_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}

            if _aggregates is not None:
                _canvas = render_plot('By Year',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates,
                                           _scenarios,
                                           _regions,
                                           _units,
                                           _vartypes,
                                           _years, scenario=_scenario,
                                           pattern_active=_pattern, text_active=_text)

        elif _p_type == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _u_style = {'display': 'block'}
            _v_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            if _aggregates is not None:
                _canvas = render_plot('Trend Over Years',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates,
                                           _scenarios,
                                           _regions,
                                           _units,
                                           _vartypes,
                                           _years, scenario=_scenario)
        elif _p_type == 'Trend in one Year':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _u_style = {'display': 'block'}
            _v_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            if _aggregates is not None:
                _canvas = render_plot('Trend in one Year',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates,
                                           _scenarios,
                                           _regions,
                                           _units,
                                           _vartypes,
                                           _years, scenario=_scenario)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _s_style = {'display': 'block'}
            _u_style = {'display': 'block'}
            _v_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            if _aggregates is not None:
                _canvas = render_plot('Pie Chart',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates,
                                           _scenarios,
                                           _regions,
                                           _units,
                                           _vartypes,
                                           _years, scenario=_scenario)

        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _u_style = {'display': 'block'}
            _v_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            if _aggregates is not None:
                _canvas = render_plot('By Region',
                                           name,
                                           data_handler.processed_data[model][name],
                                           _aggregates,
                                           _scenarios,
                                           _regions,
                                           _units,
                                           _vartypes,
                                           _years, scenario=_scenario,
                                           pattern_active=_pattern, text_active=_text)

        return _canvas, _r_style, _y_style, dash.no_update, _s_style, _m_style, _u_style, _v_style, _pattern_style, _text_style