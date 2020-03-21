from firebase_admin import credentials, firestore
import firebase_admin

import os

def get_data():
    key = eval(os.getenv("FIREBASE_CREDENTIALS"))
    cred = credentials.Certificate(key)
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    docs_in_a_dict = dict()
    for doc in docs:
        docs_in_a_dict[doc.id] = doc.to_dict()

    return docs_in_a_dict
