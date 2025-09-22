import dash
from dash import Output, Input, State, ALL, dcc

from profiles.recap.visualization_scripts.generation_supply import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Summary',
            'viz': 'Electricity Supply'
        }, 'figure'),
        Output({
            'type': 'recap-supply-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'recap-supply-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'recap-supply-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'recap-supply-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'recap-supply-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output(
            {
                'type': 'recap-supply-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'recap-supply-text-switch',
                'index': ALL
            },
            'style'
        ),
        Input({
            'type': 'recap-supply-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'recap-supply-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'recap-supply-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'recap-supply-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'recap-supply-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'recap-supply-year-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'recap-supply-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'recap-supply-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'recap-supply-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'recap-supply-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'recap-supply-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Summary',
            'viz': 'Electricity Supply'
        }, 'figure'),
        State({
            'type': 'recap-supply-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'recap-supply-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'recap-supply-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'recap-supply-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'recap-supply-text-switch',
                'index': ALL
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_supply(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _pattern, _text,
                         _download,_r_style, _y_style, _canvas, _data, _s_style, _m_style, _pattern_style, _text_style):
        #print('updating supply plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'recap-supply-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'recap-supply-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Summary']['Electricity Supply'].to_csv, "supply.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _pattern_style, _text_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'recap-supply-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['Summary']['Electricity Supply'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years', data_handler.processed_data['Summary']['Electricity Supply'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'} 
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['Summary']['Electricity Supply'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['Summary']['Electricity Supply'],
                                           _aggregates[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in _data], _s_style, _m_style, _pattern_style, _text_style