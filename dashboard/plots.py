import plotly.express as px
import pandas as pd
import datetime

col_profile = ['gender', 'isSmoker', 'testedPositiveOn', 'hasFlueVaccine',
               'hasLungDisease', 'hasDiabetes', 'isObese', 'takeSteroids']
col_symptoms = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                'hasLimbPain', 'hasSniff', 'hasDiarrhea', 'hasSoreThroat',
                'hasHeadache', 'hasBreathingProblem']


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

    df = pd.DataFrame.from_records(recs)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df


def dummy_function(data):
    import pdb
    pdb.set_trace()
    fig = px.scatter(x=range(10), y=range(10))
    return fig.to_html(full_html=False,
                       include_plotlyjs=True)  # , include_mathjax=True)


def sun_burst(data):
    today = datetime.datetime.now()
    mid = today.replace(hour=0, minute=0, second=0, microsecond=0)
    time_0 = datetime.datetime.timestamp(mid)

    col_profile = ['testedPositiveOn'
                   ]
    col_symptoms = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                    'hasLimbPain', 'hasSniff', 'hasDiarrhea', 'hasSoreThroat',
                    'hasHeadache', 'hasBreathingProblem']
    names_symptoms = {'hasCough': 'Cough', 'hasFever': 'Fever',
                      'hasChills': 'Chills', 'feelsWeak': 'Feels Weak',
                      'hasLimbPain': 'Limb Pain', 'hasSniff': 'Sniffles',
                      'hasDiarrhea': 'Diarrhea', 'hasSoreThroat': 'Sore Throat',
                      'hasHeadache': 'Headache',
                      'hasBreathingProblem': 'Breathing Problem'}

    color_map = {' ':'white', 'no Cough': 'white', 'no Fever': 'white',
                 'no Chills': 'white', 'no Feels Weak': 'white',
                 'no Limb Pain': 'white', 'no Sniffles': 'white',
                 'no Diarrhea': 'white', 'no Sore Throat': 'white',
                 'no Headache': 'white',
                 'no Breathing Problem': 'white',
                 'Cough': 'red', 'Fever': 'red',
                 'Chills': 'red', 'Feels Weak': 'red',
                 'Limb Pain': 'red', 'Sniffles': 'red',
                 'Diarrhea': 'red', 'Sore Throat': 'red',
                 'Headache': 'red',
                 'Breathing Problem': 'red','Positive Corona Test':'red','No Corona Confirmed':'white' }

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
    frame['nr_symptoms'] = frame[colnames[1:]].sum(axis=1)
    for col in colnames[1:]:
        frame[col] = frame[col].replace(True, names_symptoms[col])
        frame[col] = frame[col].replace(False, ' ')

    fig = px.sunburst(frame,
                      path=colnames, color='nr_symptoms',
                      maxdepth=6)

    return fig.to_html(full_html=False, include_plotlyjs=True)
