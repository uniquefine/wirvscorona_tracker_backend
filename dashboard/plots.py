
import plotly.express as px
import pandas as pd


def dummy_function(data):
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False, include_plotlyjs=True)#, include_mathjax=True)


def sun_burst(data):

    colnames = ['corona','cough', 'fever','pain']

    empty_line = {}
    for key in colnames:
        empty_line[key] = False

    frame = pd.DataFrame(columns=colnames)

    for key, components in data.items():
        line = empty_line.copy()
        line['corona'] = components['profile']['corona']
        for symptom, present in components['journal']['today'].items():
            if symptom in colnames:
                line[symptom] = present
            frame = frame.append(line, ignore_index=True)

    for col in colnames:
        frame[col] = frame[col].replace(True, f'has{col}')
        frame[col] = frame[col].replace(False, f'no {col}')

    fig = px.sunburst(frame, path = colnames)
    return fig.to_html(full_html=False, include_plotlyjs=True)
