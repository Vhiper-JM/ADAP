import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os  # Import the os module for path operations

# Get the current directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
json_file_path = os.path.join(current_dir, 'auto-liderazgodb-firebase-adminsdk-jtcig-7a58637b6f.json')

# Check if the JSON file exists
if os.path.isfile(json_file_path):
    # Credenciales de la base de datos
    firebase_sdk = credentials.Certificate(json_file_path)
    # Referencia a la base de datos
    firebase_admin.initialize_app(firebase_sdk, {'databaseURL': 'https://auto-liderazgodb-default-rtdb.firebaseio.com/'})
    # Referencia a la base de datos con nombre de variable descriptivo
    refDB = db.reference()
    # Print the contents of the tables in the database in an organized way
    print("Printing contents of the tables in the database:")
    for table_name in refDB.get().keys():
        table_data = refDB.child(table_name).get()
        print(f"Table: {table_name}")
        print(json.dumps(table_data, indent=4))  # Format the table data using json.dumps
else:
    print(f"Error: JSON file not found at {json_file_path}")
