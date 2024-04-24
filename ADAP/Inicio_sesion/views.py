# Django
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Models
from .models import CustomUser, Company

def index(request):
    """
    Muestra el inicio de la plataforma con el login en ingles
    """
    return redirect("Inicio_sesion:signin")

# Recordar reemplazar vew login OFICIAL
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def signin(request):
    """
    Args:
        request: La solicitud HTTP recibida.

    Returns:
        Una respuesta HTTP que renderiza la página de inicio de sesión o redirige a la página de formulario de usuario.

    Raises:
        No se producen excepciones en este código.
    """
    if request.method == 'GET':
        # Si la solicitud es GET, renderiza la página de inicio de sesión.
        return render(request, 'Inicio_sesion/login.html')
    else:
        # Si la solicitud no es GET, obtén el correo electrónico y la contraseña del formulario.
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Autentica al usuario usando el correo electrónico y la contraseña proporcionados.
        user = authenticate(username=email, password=password)
        company = Company.objects.filter(email=email)
        
        if user is not None:
            # Si el usuario es autenticado correctamente, inicia sesión en la sesión actual.
            login(request, user)
            # Redirige a la página de formulario de usuario.
            return redirect('Formulario:userView')
        else:
            # Si la autenticación falla, podrías manejar el error aquí, como mostrar un mensaje de error.
            # En este caso, se puede redirigir a la misma página de inicio de sesión con un mensaje de error.
            return render(request, 'Inicio_sesion/login.html', context={'error_message': 'Credenciales inválidas. Por favor, inténtalo de nuevo.'})


# NO OLVIDAR HACER QUE LOS HTML SE ENVIEN LA INFORMACION A SI MISMAS
def signup(request):
    if request.method == 'GET':
        return render(request, 'Inicio_sesion/signupuser.html')
    else:
        first_name = request.POST.get('name')
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
        
        company = Company.objects.filter(name=company)
        custom_user = CustomUser(
            first_name=first_name,
            last_name=lastName,
            user_id=userID,
            gender=gender,
            nationality=nationality,
            phone=phone,
            country=country,
            birthday=birthday,
            email=email,
            company=company,
            position=position,
            is_entrepreneur=isEntrepreneur,
            entrepreneurship=entrepreneurship,
            password=password,
        )
        
        custom_user.save()

        user_custom_user = User.objects.create_user(username=email, email=email, password=password)
        # TODO - Utilizar funcion login para logear, crear la cookie, y redireccionar a la view principal

        pass


def signup_business(request):
    if request.method == 'GET':
        return render(request, 'Inicio_sesion/sign_up-company.html')
    else:
        companyName = request.POST.get('companyName')
        foundationDate = request.POST.get('dateFoundation')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        country = request.POST.get('country')
        # Crear una instnancia de la empresa
        company = Company.objects.create(
            companyName=companyName,
            foundationDate=foundationDate,
            email=email,
            phone=phone,
            country=country,
            password=password  # Considerar la necesidad de hash
        )
        company.save()
        # user_company = User.objects.create_user(username=email, email=email, password=password)
        # TODO - Utilizar funcion login para logear, crear la cookie, y redireccionar a la view principal
        return redirect('Formulario:companyView')  # Redirigir a la vista del formulario de empresa
