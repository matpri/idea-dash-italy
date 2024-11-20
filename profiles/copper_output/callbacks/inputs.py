import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.inputs import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'inputs'
        }, 'figure'),
        Output({
            'type': 'copper-inputs-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'copper-inputs-vre-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-transmission-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-year-select',
            'index': ALL
        }, 'style'),

        Input({
            'type': 'copper-inputs-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-season-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-vre-variable-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-transmission-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'inputs'
        }, 'figure'),
        State({
            'type': 'copper-inputs-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'copper-inputs-vre-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-transmission-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-scenario-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'copper-inputs-scenario-multi-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'copper-inputs-extant-capacity-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-year-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_inputs(_p_type, _season, _vre_variable, t_ptype, t_year, t_scenario, t_scenarios,
                      _extant_capacity_select, _extant_capacity_region_select, _extant_capacity_year_select,
                      _extant_capacity_scenario_select, _extant_capacity_scenario_multi_select,
                      _download, _canvas, _data, _vre_style, _transmission_style, _extant_capacity_style, t_scen_style, t_scen_multi_style,
                      _extant_capacity_rep_style, _extant_capacity_scenario_select_style,
                      _extant_capacity_scenario_multi_select_style, _extant_capacity_region_select_style,
                      _extant_capacity_year_select_style):
        # Importing the data handler for processing data
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        # Handling download button click
        if 'copper-inputs-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper-inputs-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER']['Inputs'].to_csv,
                                             "inputs.csv")
            return _canvas, _data, _vre_style, _transmission_style, t_scen_style, t_scen_multi_style

        # Determine the index of the plot select input
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-inputs-plot-select')):
                idx = i
                break

        # Initialize scenario variable
        scen = []
        e_scen = []
        e_year = _extant_capacity_year_select[idx]
        e_region = _extant_capacity_region_select[idx]
        e_select = _extant_capacity_select[idx]
        # Update styles based on selected plot type
        if 'Vre Capacity Factors' in _p_type[idx]:
            _extant_capacity_style[idx] = {'display': 'none'}
            _extant_capacity_rep_style[idx] = {'display': 'none'}
            _vre_style[idx] = {'display': 'block'}
            _transmission_style[idx] = {'display': 'none'}
        elif 'Extant Transmission' in _p_type[idx]:
            _vre_style[idx] = {'display': 'none'}
            _transmission_style[idx] = {'display': 'block'}
            _extant_capacity_style[idx] = {'display': 'none'}
            _extant_capacity_rep_style[idx] = {'display': 'none'}
            if t_ptype[idx] == 'Map Plot':
                t_scen_style[idx] = {'display': 'block'}
                t_scen_multi_style[idx] = {'display': 'none'}
                scen = t_scenario[idx]
            else:
                t_scen_style[idx] = {'display': 'none'}
                t_scen_multi_style[idx] = {'display': 'block'}
                scen = t_scenarios[idx]
        elif 'Extant Capacity' in _p_type[idx]:
            _vre_style[idx] = {'display': 'none'}
            _transmission_style[idx] = {'display': 'none'}
            _extant_capacity_style[idx] = {'display': 'block'}
            _extant_capacity_rep_style[idx] = {'display': 'block'}
            if e_select == 'By Year':
                e_scen = _extant_capacity_scenario_multi_select[idx]
                _extant_capacity_scenario_select_style[idx] = {'display': 'none'}
                _extant_capacity_scenario_multi_select_style[idx] = {'display': 'block'}
                _extant_capacity_region_select_style[idx] = {'display': 'none'}
                _extant_capacity_year_select_style[idx] = {'display': 'block'}
            elif e_select == 'By Region':
                e_scen = _extant_capacity_scenario_multi_select[idx]
                _extant_capacity_scenario_select_style[idx] = {'display': 'none'}
                _extant_capacity_scenario_multi_select_style[idx] = {'display': 'block'}
                _extant_capacity_region_select_style[idx] = {'display': 'block'}
                _extant_capacity_year_select_style[idx] = {'display': 'none'}
            elif e_select == 'Trend Over Years':
                e_scen = _extant_capacity_scenario_select[idx]
                _extant_capacity_scenario_select_style[idx] = {'display': 'block'}
                _extant_capacity_scenario_multi_select_style[idx] = {'display': 'none'}
                _extant_capacity_region_select_style[idx] = {'display': 'block'}
                _extant_capacity_year_select_style[idx] = {'display': 'none'}
            else:
                e_scen = _extant_capacity_scenario_select[idx]
                _extant_capacity_scenario_select_style[idx] = {'display': 'block'}
                _extant_capacity_scenario_multi_select_style[idx] = {'display': 'none'}
                _extant_capacity_region_select_style[idx] = {'display': 'block'}
                _extant_capacity_year_select_style[idx] = {'display': 'block'}
        else:
            _vre_style[idx] = {'display': 'none'}
            _transmission_style[idx] = {'display': 'none'}

        # Render the plot based on the selected inputs
        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['COPPER']['Inputs'],
                                   _vre_variable[idx], _season[idx], t_p_type=t_ptype[idx], t_year=t_year[idx],
                                   t_scenarios=scen, e_year=e_year, e_region=e_region, e_scenarios=e_scen)

        return _canvas, [dash.no_update for _ in
                         _data], _vre_style, _transmission_style, _extant_capacity_style, t_scen_style, t_scen_multi_style, _extant_capacity_rep_style, _extant_capacity_scenario_select_style, _extant_capacity_scenario_multi_select_style, _extant_capacity_region_select_style, _extant_capacity_year_select_style
