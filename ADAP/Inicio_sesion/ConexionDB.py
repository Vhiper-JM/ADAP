import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Importar el módulo os para operaciones de ruta
import os  

# Obtener el directorio actual donde se encuentra este script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa al archivo JSON
json_file_path = os.path.join(current_dir, 'auto-liderazgodb-firebase-adminsdk-jtcig-7a58637b6f.json')

# Credenciales de la base de datos
cred = credentials.Certificate(json_file_path)

# Referencia a la base de datos
# Inicializar la aplicación Firebase si aún no está inicializada
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Referencia a la base de datos con nombre de variable descriptivo
db = firestore.client()

# Imprimir todo el contenido de la base de datos sin tener definidas las colecciones
# Obtener todas las colecciones de la base de datos
collections = db.collections()
for collection in collections:
    print(f"Collection ID: {collection.id}")
# Obtener todos los documentos de la colección
documents = collection.stream()
for document in documents:
    # Imprime el ID del documento y los datos del documento de manera ordenada y organizada
    print(f"Document ID: {document.id}")
    for key, value in document.to_dict().items():
        print(f"{key}: {value}")
        # Verificar si la variable "CORREO" está presente en el documento
    if "CORREO" in document.to_dict():
        print("Correo encontrado en el documento actual")
        correo = document.to_dict()["CORREO"]
        print(f"Correo: {correo}")

# Función para autenticación de usuario
def authenticate_user(email, password):
    try:
        # Verificar la contraseña usando la API REST de Firebase Authentication
        verify_password_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCkeIBWE--pQhFUWgJ0ownE_le1ixzJBxw"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(verify_password_url, json=data)
        if response.status_code == 200:
            print("¡Autenticación exitosa!")
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
        # Verificar en cada colección si el email existe
        print("Checking email in all collections...")
        collections = db.collections()
        for collection in collections:
            print(f"Collection ID: {collection.id}")
            # Obtener todos los documentos de la colección
            documents = collection.stream()
            for document in documents:
                # Imprime el ID del documento y los datos del documento de manera ordenada y organizada
                print(f"Document ID: {document.id}")
                if "email" in document.to_dict():
                    correo = document.to_dict()["email"]
                elif "CORREO" in document.to_dict():
                    correo = document.to_dict()["CORREO"]
                else:
                    continue
                if correo == email:
                    print("Correo encontrado en el documento actual")
                    # Impresión de depuración
                    print(f"El correo {email} existe en la colección {collection.id}")
                    return True
        return False  # El correo no existe en ninguna colección
    except Exception as e:
        print(f"Error al verificar el correo: {e}")
        return False
    
def create_document(collection_name, document_data):
    try:
        # Crear un nuevo documento en la colección con los datos proporcionados
        db.collection(collection_name).add(document_data)
        print("Documento creado exitosamente")
        return True
    except Exception as e:
        print(f"Error al crear el documento: {e}")
        return False

