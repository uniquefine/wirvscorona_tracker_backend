import random
import time
import json
import pdb

def rand_date():
    random_date = time.time() - 86400 * random.choice([0, 1, 2, 3, 4, 5, 6])
    return random_date


def generate_data(nr_users, outpath):
    col_profile = ['gender', 'testedPositiveOn', 'isSmoker', 'hasFlueVaccine',
                   'hasLungDisease', 'hasDiabetes', 'isObese', 'takeSteroids']
    col_journal = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                   'hasLimbPain', 'hasSniff', 'hasDiarrhea', 'hasSoreThroat',
                   'hasHeadache', 'hasBreathingProblem']

    data = {}
    probs = {
        'corona': {'hasCough': 0.667, 'hasFever': 0.879, 'hasChills': 0.114,
                   'feelsWeak': 0.381,
                   'hasLimbPain': 0.148, 'hasSniff': 0.048,
                   'hasDiarrhea': 0.037, 'hasSoreThroat': 0.139,
                   'hasHeadache': 0.136, 'hasBreathingProblem': 0.186},
        'flue': {'hasCough': 0.8, 'hasFever': 0.879, 'hasChills': 0.114,
                 'feelsWeak': 0.8,
                 'hasLimbPain': 0.8, 'hasSniff': 0.3, 'hasDiarrhea': 0.037,
                 'hasSoreThroat': 0.139,
                 'hasHeadache': 0.8, 'hasBreathingProblem': 0},
        'sniff': {'hasCough': 0.1, 'hasFever': 0.1, 'hasChills': 0.114,
                  'feelsWeak': 0.3,
                  'hasLimbPain': 0, 'hasSniff': 1, 'hasDiarrhea': 0.02,
                  'hasSoreThroat': 0.1,
                  'hasHeadache': 0.3, 'hasBreathingProblem': 0},
        'healthy': {'hasCough': 0, 'hasFever': 0, 'hasChills': 0,
                    'feelsWeak': 0,
                    'hasLimbPain': 0, 'hasSniff': 0, 'hasDiarrhea': 0,
                    'hasSoreThroat': 0,
                    'hasHeadache': 0.05, 'hasBreathingProblem': 0}}

    for user in range(nr_users):
        data[user] = {'profile': {}, 'journal': {}}
        data[user]['profile']['gender'] = random.choice(['male', 'female'])
        status = random.choices(['corona', 'flue', 'sniff', 'healthy'],
                               weights=[0.1, 0.2, 0.3, 0.4])[0]
        #pdb.set_trace()
        if status == 'corona':
            data[user]['profile']['testedPositiveOn'] = random.choice(
                [rand_date(), None])
        else:
            data[user]['profile']['testedPositiveOn'] = None

        for entry, value in zip(col_profile[2:],
                                random.choices([True, False], k=6)):
            data[user]['profile'][entry] = value
            if data[user]['profile']['gender'] == 'male':
                data[user]['profile']['pregnant'] = False

        dates = []
        for i in range(random.choice([1, 2, 3, 4])):
            dates += [time.time() - i * 86400]

        for date in dates:
            data[user]['journal'][date] = {}
            for entry in col_journal:
                p_t = probs[status][entry]
                value = random.choices([True, False], weights=[p_t, 1-p_t])[0]
                data[user]['journal'][date][entry] = value

    with open(outpath, 'w') as outfile:
        json.dump(data, outfile, indent=1)


generate_data(1000, 'sampledata')
