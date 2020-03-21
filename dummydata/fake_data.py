import random
import time
import json


def rand_date():
    random_date =time.time()-86400*random.choice([0,1,2,3,4,5,6])
    return random_date


def generate_data(nr_users, outpath):
    col_profile = ['gender', 'testedPositiveOn', 'isSmoker', 'hasFlueVaccine',
                   'hasLungDisease', 'hasDiabetes', 'isObese', 'takeSteroids']
    col_journal = ['hasCough', 'hasFever', 'hasChills', 'feelsWeak',
                   'hasLimbPain', 'hasSniff', 'hasDiarrhea', 'hasSoreThroat',
                   'hasHeadache', 'hasBreathingProblem']

    data = {}
    for user in range(nr_users):
        data[user] = {'profile':{}, 'journal': {}}
        data[user]['profile']['gender'] = random.choice(['Male', 'Female'])

        if random.choice([True, False]):
            data[user]['profile']['testedPositiveOn'] = rand_date()

        for entry, value in zip(col_profile[2:],
                                random.choices([True, False], k=6)):
            data[user]['profile'][entry] = value
            if data[user]['profile']['gender'] == 'Male':
                data[user]['profile']['pregnant'] = False

        dates = []
        for i in range(random.choice([1,2,3,4])):
            dates += [time.time()-i*86400]

        for date in dates:
            data[user]['journal'][date] = {}
            for entry, value in zip(col_journal, random.choices([True, False],k=10)):
                data[user]['journal'][date][entry] = value

        with open(outpath, 'w') as outfile:
            json.dump(data, outfile, indent=1)


generate_data(1000, 'sampledata.json')
