import firebase_admin
from firebase_admin import credentials, firestore
import os

# Load environment variables from .env file
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

# Firebase configuration
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
FIREBASE_ADMIN_SDK_CREDENTIALS_PATH = os.getenv('FIREBASE_ADMIN_SDK_CREDENTIALS_PATH')


# DEBBUGGING PRINT
# print(f"FIREBASE_API_KEY: {FIREBASE_API_KEY}")


# Credenciales de la base de datos
cred = credentials.Certificate(FIREBASE_ADMIN_SDK_CREDENTIALS_PATH)

# Referencia a la base de datos
# Inicializar la aplicación Firebase si aún no está inicializada
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Referencia a la base de datos con nombre de variable descriptivo
db = firestore.client()

# Imprimir todo el contenido de la base de datos sin tener definidas las colecciones
# Obtener todas las colecciones de la base de datos
collections = db.collections()


# DEBBUGGING PRINT
# for collection in collections:
#     print(f"Collection ID: {collection.id}")
# # Obtener todos los documentos de la colección
# documents = collection.stream()
# for document in documents:
#     # Imprime el ID del documento y los datos del documento de manera ordenada y organizada
#     print(f"Document ID: {document.id}")
#     for key, value in document.to_dict().items():
#         print(f"{key}: {value}")
#         # Verificar si la variable "CORREO" está presente en el documento
#     if "CORREO" in document.to_dict():
#         print("Correo encontrado en el documento actual")
#         correo = document.to_dict()["CORREO"]
#         print(f"Correo: {correo}")

# Función para autenticación de usuario
def authenticate_user(email, password):
    try:
        # Verificar la contraseña usando la API REST de Firebase Authentication
        verify_password_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        # DEBBUGGING PRINT
        # print("Verifying password...")
        # print(f"Email: {email}")
        # print(f"Password: {password}")

        response = requests.post(verify_password_url, json=data)
        if response.status_code == 200:
            # print("¡Autenticación exitosa!")
            return True
        else:
            error_message = response.json()["error"]["message"]
            # Retorna un error para manejarlo en un bloque de excepciónx
            return False
    except Exception as e:
        print(f"Fallo en la autenticación: {e}")

# Función para verificar la existencia de un correo en todas las colecciones de la base de datos
def check_email_existence(email):
    try:
        # DEBBUGGING PRINT
        # Verificar en cada colección si el email existe
        # print("Checking email in all collections...")
        collections = db.collections()
        for collection in collections:
            # print(f"Collection ID: {collection.id}")
            # Obtener todos los documentos de la colección
            documents = collection.stream()
            for document in documents:
                # Imprime el ID del documento y los datos del documento de manera ordenada y organizada
                # print(f"Document ID: {document.id}")
                if "email" in document.to_dict():
                    correo = document.to_dict()["email"]
                elif "CORREO" in document.to_dict():
                    correo = document.to_dict()["CORREO"]
                else:
                    continue
                if correo == email:
                    # print("Correo encontrado en el documento actual")
                    # Impresión de depuración
                    # print(f"El correo {email} existe en la colección {collection.id}")
                    return True
        return False  # El correo no existe en ninguna colección
    except Exception as e:
        print(f"Error al verificar el correo: {e}")
        return False
    
def create_document(collection_name, document_data):
    try:
        # Crear un nuevo documento en la colección con los datos proporcionados
        db.collection(collection_name).add(document_data)
        # print("Documento creado exitosamente")
        return True
    except Exception as e:
        print(f"Error al crear el documento: {e}")
        return False

