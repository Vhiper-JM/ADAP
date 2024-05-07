from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from Inicio_sesion.models import CustomUser, Company
from Formulario.models import Form, Section
from django.contrib.auth.models import User


def get_user_info(email):
    """
    Función para obtener información del usuario basada en el correo electrónico.
    """
    try:
        # Busca el usuario en la base de datos basado en el correo electrónico
        user = CustomUser.objects.get(email=email)
        # Imprime la información del usuario para verificar
        print(f"User Info: {user.first_name} {user.last_name}, Email: {user.email}, Phone: {user.phone}, Country: {user.country}")
        # Devuelve un diccionario con la información del usuario
        return {
            'name': user.first_name + ' ' + user.last_name,
            'email': user.email,
            'phone': user.phone,
            'country': user.country,
            # Otros campos de información del usuario según el modelo CustomUser...
        }
    except CustomUser.DoesNotExist:
        print("User not found in the database.")
        return None  # Usuario no encontrado en la base de datos

def get_company_info(email):
    try:
        # Busca la compañía en la base de datos basada en el correo electrónico
        company = Company.objects.get(email=email)
        
        # Devuelve un diccionario con la información de la compañía
        return {
            'email': company.email,
            'companyName': company.companyName,
            'foundationDate': company.foundationDate,
            'NIT': company.NIT,
            'phone': company.phone,
            'country': company.country,
        }
    except Company.DoesNotExist:
        print("Company not found in the database.")
        return None  # Compañía no encontrada en la base de datos




def index(request):
    """
    Index view
    """
    return HttpResponse("This is an index page")

def userView(request):
    """
    View for userView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get('user_email')
    if email:
        # Obtén información del usuario
        user_info = get_user_info(email)
        if user_info:
            # Pasa la información del usuario a la plantilla para renderizarla
            return render(request, 'Formulario/ViewUser.html', {'user_info': user_info})
        else:
            return HttpResponse('Error retrieving user information')
    else:
        return HttpResponse('Email not provided in session')

def companyView(request):
    """
    View for companyView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get('user_email')
    # print("User Email in Session:", email)
    if email:
        # Obtén información de la compañía
        django_user = request.user  # Assuming request.user is the Django user
        company_info = get_object_or_404(Company, email=django_user.email)
        print(company_info.email)
        if company_info:
            # Pasa la información de la compañía a la plantilla para renderizarla
            return render(request, 'Formulario/ViewCompany.html', {'company_info': company_info})
        else:
            return HttpResponse('Error retrieving company information')
    else:
        authenticatable_users = User.objects.filter(password__isnull=False).exclude(password='')
        print("Authenticatable Users:")
        for user in authenticatable_users:
            print(user.username)
        return HttpResponse('Email not provided in session')
    
def editProfile(request):
    return render(request, 'Formulario/tempEditProfile.html')
    
def uploadProfilePicture(request):
    return HttpResponse("You are trying to upload a picture")

    
def createFormView(request):
    if request.method == 'POST':
    # Handle POST request to render the create form view
        user_email = request.session.get('user_email')
        company_info = Company.objects.get(email=user_email)
        return render(request, 'Formulario/tempCreateForm.html', {'company_info': company_info})
    else:

        # Redirect to a error page or reload the current page
        return HttpResponse('Error entering form view')  # Assuming 'dashboard' is the URL name for the dashboard view

from django.shortcuts import render
from .models import Form

def createForm(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_sections = request.POST.getlist('selected_sections')  # Obtener las secciones seleccionadas
        django_user = request.user  # Assuming request.user is the Django user

        # Obtener la compañía autenticada actualmente
        company = get_object_or_404(Company, email=django_user.email)

        # Crear el formulario con los datos proporcionados
        form = Form.objects.create(
            title=title,
            company=company,
            start_date=start_date,
            end_date=end_date,
        )
        

        # Asignar las secciones seleccionadas al formulario
        for section_name in selected_sections:
            section = Section.objects.get(name=section_name)
            form.sections.add(section)

        # Renderizar la plantilla HTML con los detalles del formulario creado
        return render(request, 'Formulario/tempFormView.html', {'form': form})

    # Lógica para renderizar la página de creación de formulario si no es una solicitud POST
    return render(request, 'Formulario/tempCreateForm.html')




# Resto de las vistas...


def desempContextual(request):
    """
    View for desempenocontextual.html
    """
    return render(request, 'Formulario/desempenocontextual.html')

def desempContraproducente(request):
    """
    View for desempenocontraproducente.html
    """
    return render(request, 'Formulario/desempenocontraproducente.html')

def desempTareas(request):
    """
    View for desempenodetareas.html
    """
    return render(request, 'Formulario/desempenodetareas.html')

def estraConstructivas(request):
    """
    View for estrategiasconstructivas.html
    """
    return render(request, 'Formulario/estrategiasconstructivas.html')

def estraComportamiento(request):
    """
    View for estrategiasdecomportamiento.html
    """
    return render(request, 'Formulario/estrategiasdecomportamiento.html')

def estraRecompensa(request):
    """
    View for estrategiasderecompensa.html
    """
    return render(request, 'Formulario/estrategiasderecompensa.html')
