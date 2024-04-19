# Django
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
<<<<<<< HEAD
import firebase_admin.auth
from .ConexionDB import db, authenticate_user, check_email_existence, create_document  # Importing db reference from ConexionDB.py

import pyrebase
=======
import ConexionDB as CDB # Importing db reference from ConexionDB.py 
>>>>>>> 09cee828291f737887fd24d783202f5fa5d98091

# import firebase_admin
# import smtplib

firebaseConfig = {
    "apiKey": "AIzaSyCkeIBWE--pQhFUWgJ0ownE_le1ixzJBxw",
    "authDomain": "auto-liderazgodb.firebaseapp.com",
    "databaseURL": "https://auto-liderazgodb-default-rtdb.firebaseio.com",
    "projectId": "auto-liderazgodb",
    "storageBucket": "auto-liderazgodb.appspot.com",
    "messagingSenderId": "815578098109",
    "appId": "1:815578098109:web:7680bb79cd30766d580ad4",
    "measurementId": "G-S4GRF8BD9B"
}

def index(request):
    """
    Muestra el inicio de la plataforma con el login en ingles
    """
    return render(request, "Inicio_sesion/en/login.html")

# Recordar reemplazar vew login OFICIAL
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
    CDB.authenticate_user(email, password)

    if CDB.authenticate_user(email, password) == True:
        return render(request, 'Inicio_sesion/conexEXI.html', {'email': email})

    else:
        # Return hhhtp response with error message, wrong credentials
        return HttpResponse('Credenciales incorrectas o usuario no existe')


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


def register_user(request):
    firstName = request.POST.get('name')
    lastName = request.POST.get('surname')
    userID = request.POST.get('id')
    gender = request.POST.get('gender')
    nationality = request.POST.get('nationality')
    phone = request.POST.get('phone')
    country = request.POST.get('country')
    birthday = request.POST.get('birthdate')
    email = request.POST.get('email')
    company = request.POST.get('company')
    position = request.POST.get('position')
    isEntrepreneur = request.POST.get('isEntrepreneur', "False")
    entrepreneurship = request.POST.get('entrepreneurship')
    password = request.POST.get('password')

    # Crear un diccionario con los datos del usuario
    user_data = {
        'firstName': firstName,
        'lastName': lastName,
        'userID': userID,
        'gender': gender,
        'nationality': nationality,
        'phone': phone,
        'country': country,
        'birthday': birthday,
        'email': email,
        'company': company,
        'position': position,
        'isEntrepreneur': isEntrepreneur,
        'entrepreneurship': entrepreneurship,
        'password': password
    }

    try:
        # Verificar si el correo ya existe
        email_exists = CDB.check_email_existence(email)

        if email_exists:
            return HttpResponse('El correo con el que te intentas registrar ya existe en la base de datos')
        else:
            # Crear el usuario en la base de datos
            create_document('User', user_data)  # Call the create_document function with the appropriate arguments
            # firebase_admin.auth.create_user(email=email, password=password )                 
            firebase = pyrebase.initialize_app(firebaseConfig)

            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)

            sign = auth.sign_in_with_email_and_password(email, password)
            auth.send_email_verification(sign['idToken'])
            return render(request, 'Inicio_sesion/regisEXI.html', {'email': email})

    except Exception as e:
        # Manejar errores específicos aquí
        return render(request, 'Inicio_sesion/regisEXI.html', {'error': f'Error: {e}'})


def register_company(request):
    companyName = request.POST.get('companyName')
    foundationDate = request.POST.get('dateFoundation')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    country = request.POST.get('country')
    password = request.POST.get('password')

    print(f"Company Name: {companyName}")
    print(f"Foundation Date: {foundationDate}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    # Create a dictionary with user data
    user_data = {
        'companyName': companyName,
        'foundationDate': foundationDate,
        'email': email,
        'phone': phone,
        'country': country,
        'password': password,
    }


    try:
        # Verificar si el correo ya existe
        email_exists = CDB.check_email_existence(email)

        if email_exists:
            return HttpResponse('El correo con el que te intentas registrar ya existe en la base de datos')
        else:
            # Crear el usuario en la base de datos
            CDB.create_document('Company', user_data)  # Call the create_document function with the appropriate arguments
            return render(request, 'Inicio_sesion/regisEXI.html', {'email': email})

    except Exception as e:
        # Manejar errores específicos aquí
        return render(request, 'Inicio_sesion/regisEXI.html', {'error': f'Error: {e}'})
