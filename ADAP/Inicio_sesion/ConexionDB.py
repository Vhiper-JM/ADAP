import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Credenciales de la base de datos
firebase_sdk = credentials.Certificate('auto-liderazgodb-firebase-adminsdk-jtcig-7a58637b6f.json')
#Referencia a la base de datos
firebase_admin.initialize_app(firebase_sdk, {'databaseURL': 'https://auto-liderazgodb-default-rtdb.firebaseio.com/'})

