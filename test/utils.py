import dash_mantine_components as dmc

def bar_over_years(scenarios, regions, aggregates, title, x_axis_label, y_axis_label):
    return dmc.Text(f'bar_over_years, scenarios: {scenarios}, regions: {regions}, aggregates: {aggregates}, title: {title}, x_axis_label: {x_axis_label}, y_axis_label: {y_axis_label}')

def bar_over_regions(scenarios, aggregates, years, title, x_axis_label, y_axis_label):
    return dmc.Text(f'bar_over_regions, scenarios: {scenarios}, aggregates: {aggregates}, years: {years}, title: {title}, x_axis_label: {x_axis_label}, y_axis_label: {y_axis_label}')