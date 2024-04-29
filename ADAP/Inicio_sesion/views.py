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
    if request.method == 'GET':
        return render(request, 'Inicio_sesion/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        # print(f'El correo es {email}')
        # print(f'La contrasena es {password}')
        
        # Verifica a qué tabla pertenece el correo electrónico.
        if Company.objects.filter(email=email).exists():
            # Si el correo está en la tabla Inicio_sesion_company, el usuario es una compañía.
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session['user_email'] = email  # Set the user's email in session
                return redirect('Formulario:companyView')
            else:
                return render(request, 'Inicio_sesion/login.html', context={'error_message': 'Credenciales inválidas. Por favor, inténtalo de nuevo.'})
        else:
            # Si el correo está en la tabla Inicio_sesion_customuser, el usuario no es una compañía.
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session['user_email'] = email  # Set the user's email in session
                return redirect('Formulario:userView')
            else:
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
        user_company = User.objects.create_user(username=email, email=email, password=password)
        
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
