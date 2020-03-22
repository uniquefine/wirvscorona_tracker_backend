import plotly.express as px
import pandas as pd
import datetime

col_profile = ['gender', 'testedPositiveOn', 'isSmoker', 'hasFlueVaccine',
               'hasLungDisease', 'hasDiabetes', 'isObese', 'takeSteroids',
               'livesAlone']
col_symptoms = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                'hasLimbPain', 'hasSniff', 'hasDiarrhea', 'hasSoreThroat',
                'hasHeadache', 'hasBreathingProblem']
names_symptoms = {'hasCough': 'Husten', 'hasFever': 'Fiber',
                  'hasChills': 'Schüttelfrost', 'feelsWeak': 'Schwäche',
                  'hasLimbPain': 'Gliederschmerzen', 'hasSniff': 'Schnupfen',
                  'hasDiarrhea': 'Durchfall', 'hasSoreThroat': 'Halsschmerzen',
                  'hasHeadache': 'Kopfschmerzen',
                  'hasBreathingProblem': 'Erschwertes Atmen'}

names_profile = {'gender': 'Geschlecht', 'isSmoker': 'Raucher',
                 'testedPositiveOn': 'Positiver Corona Test am',
                 'hasFlueVaccine': 'Grippe Impfung',
                 'hasLungDisease': 'Kronische Lungenkrankheit',
                 'hasDiabetes': 'Diabetes', 'isObese': 'Übergewicht',
                 'takeSteroids': 'Steroide', 'lives alone': 'Einzelhaushalt'}


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
            recs.append(
                {"userid": user, "timestamp": timestamp, **profile, **entry})

    df = pd.DataFrame.from_records(recs, columns=['userid',
                                                  'timestamp'] + col_symptoms + col_profile)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df


def dummy_function(data):
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False,
                       include_plotlyjs=True)  # , include_mathjax=True)


def infected_cummulative(data):
    df = to_df(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    test_times = df[~df['testedPositiveOn'].isna()][
        ['userid', 'testedPositiveOn']].drop_duplicates()

    test_times['nInfected'] = test_times['testedPositiveOn'].rank()
    test_times['testedPositiveOn'] = pd.to_datetime(test_times.testedPositiveOn,
                                                    unit='s')

    test_times['percentInfected'] = test_times.nInfected / df[
        'userid'].nunique() * 100

    test_times = test_times.sort_values("testedPositiveOn")
    fig = px.line(test_times, x='testedPositiveOn', y='percentInfected')

    fig.update_layout(
        xaxis_title="Zeit",
        yaxis_title="Positiv Getestet [%]",
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=1
        ),

    )
    fig.update_yaxes(range=[0, 100])
    return fig.to_html(full_html=False,
                       include_plotlyjs=True)  # , include_mathjax=True)


def symptom_dist(data):
    df = to_df(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    most_recent = df.loc[df.groupby('userid')['timestamp'].idxmax()].filter(
        col_symptoms)
    most_recent.rename(columns=names_symptoms, inplace=True)
    frequencies = most_recent.sum() / most_recent.count()
    fig = px.bar(x=frequencies.index, y=frequencies * 100, )
    fig.update_layout(
        xaxis_title="Symptom",
        yaxis_title="Gemeldet [%]",
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=1
        ),
    )
    fig.update_yaxes(range=[0, 100])
    return fig.to_html(full_html=False,

                       include_plotlyjs=True)  # , include_mathjax=True)


def profile_dist(data):
    df = to_df(data)
    df = df.filter(col_profile[2:])
    df.rename(columns=names_profile, inplace=True)
    frequencies = df.sum() / df.count()
    fig = px.bar(x=frequencies.index, y=frequencies * 100, )
    fig.update_layout(
        xaxis_title="Eigenschaft",
        yaxis_title="Gemeldet [%]",
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=1
        ),
    )
    fig.update_yaxes(range=[0, 100])
    return fig.to_html(full_html=False,
                       include_plotlyjs=True)  # , include_mathjax=True)


def sun_burst(data):
    today = datetime.datetime.now()
    mid = today.replace(hour=0, minute=0, second=0, microsecond=0)
    time_0 = datetime.datetime.timestamp(mid)

    col_profile = ['testedPositiveOn'
                   ]

    empty_line = {}
    colnames = col_profile + col_symptoms
    for key in colnames:
        empty_line[key] = False

    frame = pd.DataFrame(columns=colnames)

    for key, components in data.items():
        line = empty_line.copy()
        components_copy = {'journal': {}, 'profile': {}}
        for timest in components['journal'].keys():
            if float(timest) > time_0:
                components_copy['journal']['today'] = components['journal'][
                    timest]

        for symptom, present in components_copy['journal']['today'].items():
            if symptom in colnames:
                line[symptom] = present
        for condition, present in components['profile'].items():
            if condition in colnames:
                line[condition] = present
        frame = frame.append(line, ignore_index=True)
    frame.testedPositiveOn.fillna(value=False, inplace=True)
    frame.loc[frame[
                  'testedPositiveOn'] != False, 'testedPositiveOn'] = 'Positive Corona Test'
    frame.loc[frame[
                  'testedPositiveOn'] == False, 'testedPositiveOn'] = 'No Corona Confirmed'
    frame['Anzahl Symptome'] = frame[colnames[1:]].sum(axis=1)
    for col in colnames[1:]:
        frame[col] = frame[col].replace(True, names_symptoms[col])
        frame[col] = frame[col].replace(False, f'Kein {names_symptoms[col]}')

    fig = px.sunburst(frame,
                      path=colnames, color='Anzahl Symptome',
                      maxdepth=6)
    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=1
        ),
    )

    return fig.to_html(full_html=False, include_plotlyjs=True)
