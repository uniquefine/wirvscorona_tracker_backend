
import plotly.express as px
import pandas as pd

col_profile = ['gender', 'isSmoker', 'testedPositiveOn', 'hasFlueVaccine', 'hasLungDisease', 'hasDiabetes', 'isObese', 'takeSteroids']
col_symptoms = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                'hasLimbPain', 'hasSniff', 'hasDiarrhea','hasSoreThroat', 'hasHeadache', 'hasBreathingProblem']

def to_df(d):
    """
    Convert firebase data to pandas Dataframe. Each journal entry corresponds to one journal entry
    :param d:
    :return:
    """
    recs = []
    for user, item in d.items():
        journal = item['journal']
        profile = item['profile']
        for timestamp, entry in journal.items():
            recs.append({"userid":user, "timestamp":timestamp, **profile, **entry})

    df = pd.DataFrame.from_records(recs)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df


def dummy_function(data):
    import pdb
    pdb.set_trace()
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False, include_plotlyjs=True)#, include_mathjax=True)


def sun_burst(data):

    colnames = ['feelsWeak', 'hasSoreThroat', 'hasSniff', 'hasCough', 'hasHeadache', 'hasLimbPain', 'hasBreathingProblems', 'hasChills', 'hasFever', 'hasDiarrhea']

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

