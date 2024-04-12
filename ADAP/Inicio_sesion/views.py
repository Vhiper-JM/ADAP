import json
import pyrebase
from django.shortcuts import render
from .ConexionDB import refDB  # Importing db reference from ConexionDB.py

app_name = 'Inicio_sesion'

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

# Recordar remplazar vew login OFICIAL
def login(request):
    return render(request, 'TempLogin.html')

# view login
def postlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = autenticacion.sign_in_with_email_and_password(email, password)
        return render(request, 'conexEXI.html', {'email': email})
    except:
        return render(request, 'TempLogin.html', {'error': 'Credenciales incorrectas'})

def signin(request):
    return render(request, 'SignUp.html')

def signin_business(request):
    return render(request, 'Company_SignUp.html')

# view create user
def create_user(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    idUser = request.POST.get('id')
    gender = request.POST.get('gender')
    nationality = request.POST.get('nationality')
    phone = request.POST.get('phone')
    country = request.POST.get('country')
    date = request.POST.get('date')
    email = request.POST.get('email')
    company = request.POST.get('company')
    position = request.POST.get('position')
    entrepreneur = request.POST.get('entrepreneur')
    entrepreneurship = request.POST.get('entrepreneurship')

    # Create a dictionary with user data
    user_data = {
        'name': name,
        'surname': surname,
        'idUser': idUser,
        'gender': gender,
        'nationality': nationality,
        'phone': phone,
        'country': country,
        'date': date,
        'email': email,
        'company': company,
        'position': position,
        'entrepreneur': entrepreneur,
        'entrepreneurship': entrepreneurship
    }


    try:
        print(user_data)
        # Reference to the Firebase Realtime Database
        print(refDB)
        
        # Retrieve user data from Firebase
        user_data_dict = refDB.child('Usuario').get()  # Retrieve JSON data as a string
        print(user_data_dict)
        
        email_exists = False
        # Check if the email already exists in users data
        for key, data in user_data_dict.items():  # Loop through dictionary items correctly
            # Imprimir key y data
            print(f'Key: {key}, Data: {data}')
            if key == 'email' and data == email:
                # Si el email ya existe, imprmir la siguiente linea
                print(f'Email ya existe: {email}')
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


def create_user2(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    idUser = request.POST.get('id')
    gender = request.POST.get('gender')
    nationality = request.POST.get('nationality')
    phone = request.POST.get('phone')
    country = request.POST.get('country')
    date = request.POST.get('date')
    email = request.POST.get('email')
    company = request.POST.get('company')
    position = request.POST.get('position')
    entrepreneur = request.POST.get('entrepreneur')
    entrepreneurship = request.POST.get('entrepreneurship')

    # Create a dictionary with user data
    user_data = {
        'name': name,
        'surname': surname,
        'idUser': idUser,
        'gender': gender,
        'nationality': nationality,
        'phone': phone,
        'country': country,
        'date': date,
        'email': email,
        'company': company,
        'position': position,
        'entrepreneur': entrepreneur,
        'entrepreneurship': entrepreneurship
    }

    try:
        # Reference to the Firebase Realtime Database
        users_ref = refDB.reference('Usuario')
        users_ref.push(user_data)  # Use set() instead of push() if you want to overwrite existing data
        return render(request, 'TempLogin.html', {'error': 'Registro exitoso'})  # Redirect to a success page
    except Exception as e:
        return render(request, 'TempLogin.html', {'error': f'Error: {e}'})  # Handle any errors during the operation
