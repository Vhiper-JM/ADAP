# Django
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
# librerias adicionales
import json
import pyrebase
# archivos locales
from .ConexionDB import refDB  # Importing db reference from ConexionDB.py

# Pyrebase initialization for user authentication
config = {
  "apiKey": "AIzaSyCkeIBWE--pQhFUWgJ0ownE_le1ixzJBxw",
  "authDomain": "auto-liderazgodb.firebaseapp.com",
  "databaseURL": "https://auto-liderazgodb-default-rtdb.firebaseio.com",
  "projectId": "auto-liderazgodb",
  "storageBucket": "auto-liderazgodb.appspot.com",
  "messagingSenderId": "815578098109",
  "appId": "1:815578098109:web:7680bb79cd30766d580ad4",
  "measurementId": "G-S4GRF8BD9B"
}

firebase = pyrebase.initialize_app(config)
autenticacion = firebase.auth()

def index(request):
    """
    Muestra el inicio de la plataforma con el login en ingles
    """
    return render(request, "Inicio_sesion/en/login.html")

# Recordar remplazar vew login OFICIAL
def login(request, lang):
    """
    Muestra el inicio de sesión según el idioma seleccionado
    """
    match lang:
        case 'es':
            return render(request, 'Inicio_sesion/es/iniciarsesion.html')
        case 'en':
            return render(request, 'Inicio_sesion/en/login.html')

# view login
def postlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = autenticacion.sign_in_with_email_and_password(email, password)
        return render(request, 'Inicio_sesion/conexEXI.html', {'email': email})
    except:
        return HttpResponse('Algo salio mal')

def signup(request, lang):
    """
    Muestra el formulario de registro segun el idioma dado
    """
    match lang:
        case 'es':
            return render(request, 'Inicio_sesion/es/registrousuario.html')
        case 'en':
            return render(request, 'Inicio_sesion/en/signupuser.html')

def signup_business(request, lang):
    """
    Muestra el formulario de registro de empresa segun el idioma
    """
    match lang:
        case 'es':
            return render(request, 'Inicio_sesion/es/empresa_registro.html')
        case 'en':
            return render(request, 'Inicio_sesion/en/sign_up-company.html')


# view create user
def create_user(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    idUser = request.POST.get('id')
    gender = request.POST.get('gender')
    nationality = request.POST.get('nationality')
    phone = request.POST.get('phone')
    country = request.POST.get('country')
    birthdate = request.POST.get('birthdate')
    email = request.POST.get('email')
    company = request.POST.get('company')
    position = request.POST.get('position')
    entrepreneur = request.POST.get('entrepreneur')
    entrepreneurship = request.POST.get('entrepreneurship')
    password = request.POST.get('password')

    # Create a dictionary with user data
    user_data = {
        'name': name,
        'surname': surname,
        'idUser': idUser,
        'gender': gender,
        'nationality': nationality,
        'phone': phone,
        'country': country,
        'birthdate': birthdate,
        'email': email,
        'company': company,
        'position': position,
        'entrepreneur': entrepreneur,
        'entrepreneurship': entrepreneurship,
        'password': password
    }


    try:
        # print(user_data)
        # # Reference to the Firebase Realtime Database
        # print(refDB)
        
        # Retrieve user data from Firebase
        user_data_dict = refDB.child('Usuario').get()  # Retrieve JSON data as a string
        # print(user_data_dict)
        
        email_exists = False
        # Check if the email already exists in users data
        for key, data in user_data_dict.items():  # Loop through dictionary items correctly
            # Imprimir key y data
            # print(f'Key: {key}, Data: {data}')
            if key == 'email' and data == email:
                # Si el email ya existe, imprmir la siguiente linea
                # print(f'Email ya existe: {email}')
                email_exists = True
                break 

        if email_exists:
            return render(request, 'TempLogin.html', {'error': 'Usuario ya existe'})
        else:
            refDB.child('Usuario').push(user_data)
            return render(request, 'TempLogin.html', {'error': 'Registro exitoso'})

    except Exception as e:
        # Log or handle exceptions more specifically
        return render(request, 'TempLogin.html', {'error': f'Error: {e}'})


def create_userB(request):
    company_name = request.POST.get('companyName')
    date_of_foundation = request.POST.get('dateFoundation')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    country = request.POST.get('country')
    password = request.POST.get('password')

    # Create a dictionary with user data
    user_data = {
        'companyName': company_name,
        'dateOfFoundation': date_of_foundation,
        'email': email,
        'phone': phone,
        'country': country,
        'password': password,
    }

    try:
        # Reference to the Firebase Realtime Database
        refDB.reference('Empresa').push(user_data)  # Use set() instead of push() if you want to overwrite existing data
        return render(request, 'TempLogin.html', {'error': 'Registro exitoso'})  # Redirect to a success page
    except Exception as e:
        return render(request, 'TempLogin.html', {'error': f'Error: {e}'})  # Handle any errors during the operation
