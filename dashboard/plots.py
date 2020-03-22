
import plotly.express as px
import pandas as pd
import datetime

def dummy_function(data):
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False, include_plotlyjs=True)#, include_mathjax=True)


def sun_burst(data):

    col_profile = ['gender', 'isSmoker', 'testedPositiveOn', 'hasFlueVaccine', 'hasLungDisease', 'hasDiabetes', 'isObese', 'takeSteroids']
    col_symptoms = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                    'hasLimbPain', 'hasSniff', 'hasDiarrhea','hasSoreThroat', 'hasHeadache', 'hasBreathingProblem']
    empty_line = {}
    colnames = col_profile + col_symptoms
    for key in colnames:
        empty_line[key] = False

    frame = pd.DataFrame(columns=colnames)

    for key, components in data.items():
        line = empty_line.copy()

        for symptom, present in components['journal']['today'].items():
            if symptom in colnames:
                line[symptom] = present
        for condition, present in components['profile']
            if condition in colnames:
                line[condition] = present
        frame = frame.append(line, ignore_index=True)

    frame['hasCorona'] = bool(frame['testedPositiveOn'])
    for col in colnames[0:1,3:]:
        frame[col] = frame[col].replace(True, f'has{col}')
        frame[col] = frame[col].replace(False, f'no {col}')

    fig = px.sunburst(frame, path = colnames)
    return fig.to_html(full_html=False, include_plotlyjs=True)

