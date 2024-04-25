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


def signup(request):
    if request.method == 'GET':
        return render(request, 'Inicio_sesion/signupuser.html')
    else:
        email = request.POST.get('email')        
        existing_user = User.objects.filter(email=email).exists()        

        if existing_user:
            return render(request, 'Inicio_sesion/signupuser.html', {'error_message': 'El correo electrónico ya está registrado'})
        
        # Si no hay un usuario con el mismo correo, proceder con el registro
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        identification = request.POST.get('id')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        birthday = request.POST.get('birthdate')
        company_name = request.POST.get('company')
        position = request.POST.get('position')
        is_entrepreneur = request.POST.get('isEntrepreneur', "False")
        entrepreneurship = request.POST.get('entrepreneurship')
        password = request.POST.get('password')
        
        existing_company = Company.objects.filter(companyName=company_name).exists()
    # PARA LOS MUCHACHOS DE DOCUMENTACION
    # Antes de que se puedan registrar los usuarios (empleados), la compañia debe estar registrada
    # para que el usuario pueda registrarse bajo una compañia

        if not existing_company:
            return render(request, 'Inicio_sesion/signupuser.html', {'error_message': 'La compañia no existe'})
          
        company = Company.objects.filter(companyName=company_name).first()
        custom_user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            identification=identification,
            gender=gender,
            nationality=nationality,
            phone=phone,
            country=country,
            birthday=birthday,
            email=email,
            company=company,
            position=position,
            is_entrepreneur=is_entrepreneur,
            entrepreneurship=entrepreneurship,
            password=password,
        )
        
        custom_user.save()

        # Crear el usuario en Django
        # user_custom_user = User.objects.create_user(username=email, email=email, password=password)
        
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Formulario:companyView')  # Redirigir a la vista principal
        else:
            # Manejar el caso de autenticación fallida
            return render(request, 'Inicio_sesion/signupuser.html', {'error_message': 'Error en la autenticación'})


def signup_business(request):
    if request.method == 'GET':
        return render(request, 'Inicio_sesion/sign_up-company.html')
    else:
        companyName = request.POST.get('companyName')
        foundationDate = request.POST.get('dateFoundation')
        email = request.POST.get('email')
        existing_user = User.objects.filter(email=email).exists()
        if existing_user:
            return render(request, 'Inicio_sesion/sign_up-company.html', {'error_message': 'Error en la autenticación'})
        NIT = request.POST.get('NIT')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        country = request.POST.get('country')
        
        # Crear una instancia de la empresa
        company = Company.objects.create(
            companyName=companyName,
            foundationDate=foundationDate,
            email=email,
            NIT=NIT,
            phone=phone,
            country=country,
            password=password  # Considerar la necesidad de hash
        )
        company.save()
        
        # Crear un usuario asociado a la empresa (opcional)
        # user_company = User.objects.create_user(username=email, email=email, password=password)
        
        # Autenticar al usuario y redirigir a la vista principal
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Formulario:companyView')  # Redirigir a la vista del formulario de empresa
        else:
            # Manejar el caso de autenticación fallida
            return render(request, 'Inicio_sesion/sign_up-company.html', {'error_message': 'Error en la autenticación'})

def signout(request):
    """
    Vista para cerrar sesión de un usuario.
    """
    logout(request)  # Cierra la sesión actual del usuario
    return redirect('Inicio_sesion:index')  # Redirige a la página de inicio de sesión
