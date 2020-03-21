import firebase_admin
from firebase_admin import credentials, firestore

# Depending on where you save your key, update this
# TODO: store this safely
PATH_TO_KEY = "../covid19journalapp-firebase-adminsdk-1ce2y-1b3571ca42.json"

cred = credentials.Certificate(PATH_TO_KEY)
firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection(u'users')
docs = users_ref.stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
