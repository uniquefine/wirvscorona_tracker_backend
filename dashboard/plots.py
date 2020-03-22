
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

    df = pd.DataFrame.from_records(recs, columns=['userid', 'timestamp']+col_symptoms+col_profile)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df


def dummy_function(data):
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False, include_plotlyjs=True)#, include_mathjax=True)

def infected_cummulative(data):
    df = to_df(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    test_times = df[~df['testedPositiveOn'].isna()][['userid', 'testedPositiveOn']].drop_duplicates()

    test_times['nInfected'] = test_times['testedPositiveOn'].rank()
    test_times['testedPositiveOn'] = pd.to_datetime(test_times.testedPositiveOn, unit='s')

    test_times['percentInfected'] = test_times.nInfected / df['userid'].nunique() * 100

    test_times = test_times.sort_values("testedPositiveOn")
    fig = px.line(test_times, x='testedPositiveOn', y='percentInfected')

    fig.update_layout(
        title="Cummulative Plot of Positive tested",
        xaxis_title="Time",
        yaxis_title="Tested positive [%]",
    )
    fig.update_yaxes(range=[0, 100])
    return fig.to_html(full_html=False, include_plotlyjs=True)#, include_mathjax=True)

def symptom_dist(data):
    df = to_df(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    most_recent = df.loc[df.groupby('userid')['timestamp'].idxmax()].filter(col_symptoms)
    frequencies = most_recent.sum() / most_recent.count()
    fig = px.bar(x=frequencies.index, y=frequencies * 100, )
    fig.update_layout(
        title="Most Recent Symptom Frequency",
        xaxis_title="Symptom",
        yaxis_title="Reported [%]",
    )
    fig.update_yaxes(range=[0, 100])
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

