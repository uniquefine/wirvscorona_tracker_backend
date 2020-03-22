from firebase_admin import credentials, firestore
import firebase_admin
import json

import os
filedir = os.path.dirname(os.path.realpath(__file__))

# key = eval(os.getenv("FIREBASE_CREDENTIALS"))
# cred = credentials.Certificate(key)
# firebase_admin.initialize_app(cred)
# db = firestore.client()
#

def get_data():

    # users_ref = db.collection(u'users')
    # docs = users_ref.stream()

    # docs_in_a_dict = dict()
    # for doc in docs:
    #     docs_in_a_dict[doc.id] = doc.to_dict()

    # return docs_in_a_dict
    return json.load(open(filedir + "/../dummydata/sampledata.json", 'r'))
