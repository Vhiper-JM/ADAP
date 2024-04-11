from django.shortcuts import render
import pyrebase

app_name = 'Inicio_sesion'

# Conexion FireBase
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

firebase = pyrebase.initialize_app(firebaseConfig)
autenticacion = firebase.auth()
database = firebase.database()

# Recordar remplazar vew login OFICIAL
def login(request):
    return render(request, 'TempLogin.html')

# vew login
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
