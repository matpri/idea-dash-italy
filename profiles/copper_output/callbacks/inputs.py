import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.inputs import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'COPPER',
            'viz': 'Inputs'
        }, 'figure'),
        Output({
            'type': 'copper-inputs-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'copper-inputs-policy-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-vre-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-params-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-transmission-cost-widget',
            'index': ALL
        }, 'style'),

        Output({
            'type': 'copper-inputs-extant-capacity-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-extant-capacity-region-select',
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
            'type': 'copper-inputs-cost-widget',
            'index': ALL
        }, 'style'),

        Output({
            'type': 'copper-inputs-demand-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-demand-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-demand-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-demand-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-demand-date-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-demand-month-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-demand-year-select',
            'index': ALL
        }, 'style'),

        Output({
            'type': 'copper-inputs-transmission-widget',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'copper-inputs-scenario-select',
            'index': ALL
        }, 'style'),
        ############################
        Input({
            'type': 'copper-inputs-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-policy-scenario-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper-inputs-policy-scenario-select',
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
            'type': 'copper-inputs-params-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-params-variable-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper-inputs-transmission-cost-scenario-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper-inputs-extant-capacity-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-extant-capacity-region-select',
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
            'type': 'copper-inputs-cost-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-cost-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-cost-region-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper-inputs-demand-plot-type-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-time_step-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-date-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-month-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-demand-year-select',
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
            'type': 'copper-inputs-download-button',
            'index': ALL
        }, 'n_clicks'),
        ############################
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'COPPER',
            'viz': 'Inputs'
        }, 'figure'),
        State({
            'type': 'copper-inputs-download',
            'index': ALL
        }, 'data'),

        State({
            'type': 'copper-inputs-policy-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-vre-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-params-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-transmission-cost-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-extant-capacity-region-select',
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
            'type': 'copper-inputs-cost-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-date-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-month-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-demand-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-transmission-widget',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'copper-inputs-scenario-select',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_inputs(_p_type,
                      _policy_scenarios,
                      _vre_scenarios, _seasons, _v_type,
                      _params_scenarios, _params_variable,
                      _transmission_cost_scenarios,
                      _extant_capacity_rep, _extant_capacity_year, _extant_capacity_region, _extant_capacity_scenario,
                      _extant_capacity_scenarios,
                      _c_type, _c_scenario, _c_region,
                      _demand_plot_type,_demand_scenario,_demand_multi_scenario, _demand_region, _demand_timestep, _demand_date, _demand_month, _demand_year,
                      _t_type, _t_year, _t_scenario, _t_scenarios,
                      _download, _canvas, _data,
                      _policy_style, _vre_style, _params_style, _transmission_cost_style,
                      _extant_capacity_widget_style, _extant_capacity_year_style, _extant_capacity_region_style,
                      _extant_capacity_scenario_style, _extant_capacity_scenarios_style,
                      _cost_style,
                      _demand_widget_style,_demand_region_style, _demand_scenario_style,_demand_multi_scenario_style, _demand_date_style, _demand_month_style, _demand_year_style,
                      _transmission_style, _transmission_scenarios_style, _transmission_scenario_style

                      ):
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
            return (
                _canvas, _data, _policy_style, _vre_style, _params_style, _transmission_cost_style,
                _extant_capacity_widget_style, _extant_capacity_year_style, _extant_capacity_region_style,
                _extant_capacity_scenario_style, _extant_capacity_scenarios_style, _cost_style,
                _demand_widget_style, _demand_region_style,_demand_scenario_style,_demand_multi_scenario_style, _demand_date_style, _demand_month_style, _demand_year_style,
                _transmission_style, _transmission_scenarios_style, _transmission_scenario_style
            )

        # Determine the index of the plot select input
        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-inputs-plot-select')):
                idx = i
                break

        _policy_style[idx] = {'display': 'none'}
        _vre_style[idx] = {'display': 'none'}
        _params_style[idx] = {'display': 'none'}
        _transmission_cost_style[idx] = {'display': 'none'}
        _extant_capacity_widget_style[idx] = {'display': 'none'}
        _cost_style[idx] = {'display': 'none'}
        _demand_widget_style[idx] = {'display': 'none'}
        _transmission_style[idx] = {'display': 'none'}

        e_scen = []
        e_year = _extant_capacity_year[idx]
        e_region = _extant_capacity_region[idx]
        e_rep = _extant_capacity_rep[idx]

        if _p_type[idx] == 'Policy':
            _policy_style[idx] = {'display': 'block'}
        elif _p_type[idx] == 'Vre Capacity Factors':
            _vre_style[idx] = {'display': 'block'}
        elif _p_type[idx] == 'Technology Parameter':
            _params_style[idx] = {'display': 'block'}
        elif _p_type[idx] == 'Transmission Costs':
            _transmission_cost_style[idx] = {'display': 'block'}
        elif _p_type[idx] == 'Cost':
            _cost_style[idx] = {'display': 'block'}
        elif _p_type[idx] == 'Extant Transmission':
            _transmission_style[idx] = {'display': 'block'}
            if _t_type[idx] == 'Map Plot':
                _transmission_scenario_style[idx] = {'display': 'block'}
                _transmission_scenarios_style[idx] = {'display': 'none'}
            else:
                _transmission_scenario_style[idx] = {'display': 'none'}
                _transmission_scenarios_style[idx] = {'display': 'block'}
        elif _p_type[idx] == 'Demand':
            _demand_widget_style[idx] = {'display': 'block'}
            if _demand_plot_type[idx] == 'By Scenario':
                _demand_scenario_style[idx] = {'display': 'none'}
                _demand_multi_scenario_style[idx] = {'display': 'block'}
                _demand_region_style[idx] = {'display': 'block'}
            else:
                _demand_scenario_style[idx] = {'display': 'block'}
                _demand_multi_scenario_style[idx] = {'display': 'none'}
                _demand_region_style[idx] = {'display': 'none'}

            ts = _demand_timestep[idx]
            if ts == 'yearly':
                _demand_year_style[idx] = {'display': 'none'}
                _demand_month_style[idx] = {'display': 'none'}
                _demand_date_style[idx] = {'display': 'none'}
            elif ts == 'monthly':
                _demand_year_style[idx] = {'display': 'block'}
                _demand_month_style[idx] = {'display': 'none'}
                _demand_date_style[idx] = {'display': 'none'}
            elif ts == 'daily':
                _demand_year_style[idx] = {'display': 'block'}
                _demand_month_style[idx] = {'display': 'block'}
                _demand_date_style[idx] = {'display': 'none'}
            else:
                _demand_year_style[idx] = {'display': 'block'}
                _demand_month_style[idx] = {'display': 'block'}
                _demand_date_style[idx] = {'display': 'block'}

        elif _p_type[idx] == 'Extant Capacity':
            _extant_capacity_widget_style[idx] = {'display': 'block'}
            _extant_capacity_year_style[idx] = {'display': 'none'}
            _extant_capacity_region_style[idx] = {'display': 'none'}
            _extant_capacity_scenario_style[idx] = {'display': 'none'}
            _extant_capacity_scenarios_style[idx] = {'display': 'none'}

            if e_rep == 'By Year':
                _extant_capacity_region_style[idx] = {'display': 'block'}
                _extant_capacity_scenarios_style[idx] = {'display': 'block'}
                e_scen = _extant_capacity_scenarios[idx]
            elif _extant_capacity_rep[idx] == 'By Region':
                _extant_capacity_year_style[idx] = {'display': 'block'}
                _extant_capacity_scenarios_style[idx] = {'display': 'block'}
                e_scen = _extant_capacity_scenarios[idx]
            elif _extant_capacity_rep[idx] == 'Trend Over Years':
                _extant_capacity_region_style[idx] = {'display': 'block'}
                _extant_capacity_scenario_style[idx] = {'display': 'block'}
                e_scen = _extant_capacity_scenario[idx]
            else:
                _extant_capacity_year_style[idx] = {'display': 'block'}
                _extant_capacity_region_style[idx] = {'display': 'block'}
                _extant_capacity_scenario_style[idx] = {'display': 'block'}
                e_scen = _extant_capacity_scenario[idx]

        # Render the plot based on the selected inputs
        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['COPPER']['Inputs'],
                                   _policy_scenarios=_policy_scenarios[idx],
                                   vre_scenario=_vre_scenarios[idx], season=_seasons[idx], vre_variable=_v_type[idx],
                                   _p_variable=_params_variable[idx], _p_scenario=_params_scenarios[idx],
                                   _t_cost_scenarios=_transmission_cost_scenarios[idx],
                                   e_p_type=e_rep, e_scenarios=e_scen, e_region=e_region, e_year=e_year,
                                   _c_type=_c_type[idx], _c_scenario=_c_scenario[idx], _c_region=_c_region[idx],
                                  _demand_plot_type=_demand_plot_type[idx], _demand_region=_demand_region[idx],_demand_multi_scenario=_demand_multi_scenario[idx],
                                   _demand_scenario=_demand_scenario[idx], _demand_year=_demand_year[idx],
                                   _demand_month=_demand_month[idx], _demand_date=_demand_date[idx],
                                   _demand_time_step=_demand_timestep[idx],
                                   t_p_type=_t_type[idx],
                                   t_scenarios=_t_scenario[idx] if _t_type[idx] == 'Map Plot' else _t_scenarios[idx],
                                   t_year=_t_year[idx]
                                   )

        return (_canvas, [dash.no_update for _ in
                          _data], _policy_style, _vre_style, _params_style, _transmission_cost_style,
                _extant_capacity_widget_style, _extant_capacity_year_style, _extant_capacity_region_style,
                _extant_capacity_scenario_style, _extant_capacity_scenarios_style, _cost_style,
                _demand_widget_style, _demand_region_style,_demand_scenario_style,_demand_multi_scenario_style, _demand_date_style, _demand_month_style, _demand_year_style,
                _transmission_style, _transmission_scenarios_style, _transmission_scenario_style
                )
