
import plotly.graph_objects as go
from profiles.recap.utils import get_color


def plot(df, scenario, region, year, title, name):

    data = df[(df['scenario'] == scenario) & (df['region'] == region) & (df['time'] == year)]

    data = data[data.variable.str.contains('.')]
    if 'service' not in data.columns:
        data['service'] = data['variable']
        data['parent_service'] = data['variable'].apply(lambda x: '.'.join(x.split('.')[:-1]))

        data = data[['parent_service', 'service', 'value', 'context']]

    nodes = []
    for i, row in data.iterrows():
        if row['service'] not in nodes:
            nodes.append(row['service'])
        if row['parent_service'] not in nodes:
            nodes.append(row['parent_service'])
    data['source_int'] = data['service'].apply(lambda x: nodes.index(x))
    data['target_int'] = data['parent_service'].apply(lambda x: nodes.index(x))

    colors = [get_color(context) for context in data['context'].unique().tolist()]
    context_colors = dict(zip(data['context'].unique().tolist(), colors))
    contexts = data['context'].unique().tolist()

    fig = go.Figure(data=[go.Sankey(
        arrangement='perpendicular',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes

        ),
        link=dict(
            source=data['source_int'].tolist(),
            target=data['target_int'].tolist(),
            value=data['value'].tolist(),
            color=data['context'].apply(lambda x: context_colors[x]).tolist(),
        )
    )])

    for context in contexts:
        fig.add_scatter(x=[0], y=[0], mode='markers', marker=dict(color=context_colors[context], size=10),
                        showlegend=True, name=context)

    fig.update_layout(title_text=title,  font_size=10)
    return fig