import dash
from dash import Output, Input, State, ALL, dcc

from profiles.silver_output.visualization_scripts.map_plots import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'map_plots'
        }, 'figure'),
        Output({
            'type': 'silver-map_plots-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'silver-map_plots-date-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'silver-map_plots-date-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'silver-map_plots-time-slider',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'silver-map_plots-time-slider',
            'index': ALL
        }, 'marks'),
        Output({
            'type': 'silver-map_plots-time-slider',
            'index': ALL
        }, 'max'),
        Output({
            'type': 'silver-map_plots-time-slider-output',
            'index': ALL
        }, 'style'),
        Input({
            'type': 'silver-map_plots-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-time_step-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-date-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-time-slider',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'map_plots'
        }, 'figure'),
        State({
            'type': 'silver-map_plots-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'silver-map_plots-date-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'silver-map_plots-time-slider',
            'index': ALL
        }, 'marks'),
        State({
            'type': 'silver-map_plots-time-slider',
            'index': ALL
        }, 'max'),State({
            'type': 'silver-map_plots-time-slider-output',
            'index': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_map_plots(_p_type, _scenario, _ts, _date, _time, _download, _canvas, _data, _date_data, _time_marks, _max, _style):
        print('updating map_plots plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'silver-map_plots-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'silver-map_plots-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['SILVER Output']['Map Plots'].to_csv, "map_plots.csv")
            return _canvas, _data

        if 'silver-map_plots-time_step-select' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'silver-time_step-date-select')):
                    idx = i
                    break

            # Get the selected time step
            selected_time_step = _ts[idx]
            df = data_handler.processed_data['SILVER Output']['Map Plots']
            scen_df = df[(df['scenario'] == _scenario[idx]) & (df['classes'] == _p_type[idx])].copy()

            if selected_time_step == 'hourly':

                dates = sorted(scen_df['time'].dt.strftime('%Y-%m-%d').unique().tolist())
                date = dates[0]

                # Get the unique values of the time column during the date and sort them
                unique_times = sorted(scen_df[scen_df['time'].dt.strftime('%Y-%m-%d') == date]['time'].unique().tolist())

                date_marks = {
                    i: {'label': time.strftime('%H:%M'), 'style': {'transform': 'rotate(90deg) translate(20px, -10px)'}}
                    for i, time in enumerate(unique_times)
                    if i % 4 == 0  # Show every 4th mark
                }

                _date[idx] = date
                _time[idx] = 0
                _date_data[idx] = [{'label': date, 'value': date} for date in dates]
                _time_marks[idx] = date_marks
                _max[idx] = len(unique_times) - 1

            elif selected_time_step == 'daily':
                dates = sorted(scen_df['time'].dt.strftime('%Y-%m').unique().tolist())
                date = dates[0]
                _date[idx] = date
                _time[idx] = 0

                unique_times = sorted(scen_df[scen_df['time'].dt.strftime('%Y-%m') == date]['time'].dt.strftime('%Y-%m-%d').unique().tolist())

                date_marks = {
                    i: {'label': time.split('-')[-1], 'style': {'transform': 'rotate(90deg) translate(20px, -10px)'}}
                    for i, time in enumerate(unique_times)
                    if i % 4 == 0  # Show every 4th mark
                }
                _date_data[idx] = [{'label': date, 'value': date} for date in dates]
                _time_marks[idx] = date_marks
                _max[idx] = len(unique_times) - 1

            elif selected_time_step == 'monthly':
                dates = sorted(scen_df['time'].dt.strftime('%Y').unique().tolist())
                date = dates[0]
                _date[idx] = date
                _time[idx] = 0

                unique_times = sorted(scen_df[scen_df['time'].dt.strftime('%Y') == date]['time'].dt.strftime('%Y-%b').unique().tolist())
                date_marks = {
                    i: {'label': time.split('-')[-1], 'style': {'transform': 'rotate(90deg) translate(20px, -10px)'}}
                    for i, time in enumerate(unique_times)
                    if i % 4 == 0  # Show every 4th mark
                }
                _date_data[idx] = [{'label': date, 'value': date} for date in dates]
                _time_marks[idx] = date_marks
                _max[idx] = len(unique_times) - 1

            elif selected_time_step == 'yearly':
                _style[idx] = {'display': 'none'}
                return _canvas, [dash.no_update for _ in _data], [dash.no_update for _ in _date], [dash.no_update for _ in _date], [dash.no_update for _ in _time], [dash.no_update for _ in _time], [dash.no_update for _ in _time], _style

            else:
                return _canvas, [dash.no_update for _ in _data], [dash.no_update for _ in _date], [dash.no_update for _ in _date], [dash.no_update for _ in _time], [dash.no_update for _ in _time], [dash.no_update for _ in _time], [dash.no_update for _ in _style]

            if len(unique_times)>1:
                _style[idx] = {'display': 'block'}
            else:
                _style[idx] = {'display': 'none'}

            _canvas[idx] = render_plot(_p_type[idx], scen_df, _scenario[idx], unique_times[_time[idx]], time_size=_ts[idx])


            return _canvas, [dash.no_update for _ in _data], _date, _date_data, _time, _time_marks, _max, _style






        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] in ['silver-map_plots-plot-select', 'silver-map_plots-scenario-select',
                                          'silver-map_plots-time_step-select', 'silver-map_plots-date-select',
                                          'silver-map_plots-time-slider'])):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        # Get the selected date
        selected_date = _date[idx]

        # Get the unique times for the selected date
        unique_times = sorted(data_handler.processed_data['SILVER Output']['Map Plots'][
            data_handler.processed_data['SILVER Output']['Map Plots']['time'].dt.strftime('%Y-%m-%d') == selected_date
        ]['time'].unique().tolist())

        # Get the selected time
        selected_time = unique_times[_time[idx]]

        selected_date_time = f'{selected_date} {selected_time}'

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['SILVER Output']['Map Plots'], 
                                   _scenario[idx], selected_time, time_size=_ts[idx])

        return _canvas, [dash.no_update for _ in _data], [dash.no_update for _ in _date], [dash.no_update for _ in _date], [dash.no_update for _ in _time], [dash.no_update for _ in _time], [dash.no_update for _ in _time]
