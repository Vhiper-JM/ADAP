import json
from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from Inicio_sesion.models import CustomUser, Company
from Formulario.models import Form, Section, FormSection
from django.contrib.auth.models import User
from .models import Form, Question, Response





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
    email = request.session.get("user_email")
    if email:
        # Obten informacion del usuario
        user_info = CustomUser.objects.get(email=email)        
        # Convertir la información del usuario en un diccionario para poder pasarla a la plantilla
        
        # Obtener el listado de formularios a los que el usuario tiene acceso
        forms = Form.objects.filter(authorized_employees=user_info)
        # Convertir el queryset de formularios en una lista de diccionarios con título y fecha de finalización para poder pasarlo a la plantilla
        forms = [{"title": form.title, "end_date": form.end_date} for form in forms]
        print("Forms:", forms)
        
        responses = Response.objects.filter(employee=user_info)
        
        # Unanswered forms
        unanswered_forms = Form.objects.exclude(responses__employee=user_info)
        
        user_info_dict = {
            "first_name": user_info.first_name,
            "last_name": user_info.last_name,
            "identification": user_info.identification,
            "gender": user_info.gender,
            "nationality": user_info.nationality,
            "country": user_info.country,
            "birthday": user_info.birthday,
            "email": user_info.email,
            "company": user_info.company.companyName,
            "position": user_info.position,
            "phone": user_info.phone,
            "forms": forms,
            responses: responses
        }
        if user_info:
            # Pasa la información del usuario a la plantilla para renderizarla
            return render(request, "Formulario/ViewUser.html", {"user_info": user_info_dict})
        else:
            return HttpResponse("Error retrieving user information")
    else:
        return HttpResponse("Email not provided in session")


def companyView(request):
    """
    View for companyView.html
    """
    # Obtén el correo electrónico de la sesión
    email = request.session.get("user_email")
    # print("User Email in Session:", email)
    if email:
        # Obtén información de la compañía
        company = Company.objects.get(email=email)
        # Obtén todos los empleados de la compañía
        employees = CustomUser.objects.filter(company_id=company)
        # Turn the employees queryset into a list of dictionaries with name and position so it can be passed to the template
        employees = [
            {"name": employee.first_name + " " + employee.last_name, "position": employee.position}
            for employee in employees
        ]
        print("Employees:", employees)
        # Obten todos los formularios de la compañía
        forms = Form.objects.filter(company=company)
        # Turn the forms queryset into a list of dictionaries with title and end date so it can be passed to the template
        forms = [{"title": form.title, "end_date": form.end_date} for form in forms]
        
        context = {
            "company_info": company,
            "employees": employees,
            "forms": forms,
        }
        
        if company:
            # Pasa la información de la compañía a la plantilla para renderizarla
            print("Context:", {"company_info": company, "employees": employees})
            return render(
                request, "Formulario/ViewCompany.html", context
            )
        else:
            return HttpResponse("Error retrieving company information")
    else:
        authenticatable_users = User.objects.filter(password__isnull=False).exclude(
            password=""
        )
        print("Authenticatable Users:")
        for user in authenticatable_users:
            print(user.username)
        return HttpResponse("Email not provided in session")


def editProfile(request):
    return render(request, "Formulario/tempEditProfile.html")


def uploadProfilePicture(request):
    return HttpResponse("You are trying to upload a picture")


def createFormView(request):
    if request.method == "POST":
        # Handle POST request to render the create form view
        user_email = request.session.get("user_email")
        company_info = Company.objects.get(email=user_email)
        return render(
            request, "Formulario/tempCreateForm.html", {"company_info": company_info}
        )
    else:

        # Redirect to a error page or reload the current page
        return HttpResponse(
            "Error entering form view"
        )  # Assuming 'dashboard' is the URL name for the dashboard view

def createForm(request):
    if request.method == "POST":
        # Obtener los datos del formulario enviado por el usuario
        title = request.POST.get("title")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        selected_sections = request.POST.getlist(
            "selected_sections[]"
        )  # Obtener las secciones seleccionadas
        print("Selected Sections:", selected_sections)
        django_user = request.user  # Assuming request.user is the Django user

        # Obtener la compañía autenticada actualmente
        company = get_object_or_404(Company, email=django_user.email)

        # Convertir el JSON de empleados autorizados a una lista de correos electrónicos
        employee_emails_json = request.POST.get("employee_emails")
        # Imprimir la lista completa de correos electrónicos para verificar
        print("Employee Emails JSON:", employee_emails_json)
        employee_emails = (
            json.loads(employee_emails_json) if employee_emails_json else []
        )
        print("Employee Emails List:", employee_emails)

        # Crear el formulario con los datos proporcionados
        form = Form.objects.create(
            title=title,
            company=company,
            start_date=start_date,
            end_date=end_date,
        )

        # Agregar secciones seleccionadas al formulario a partir del identificador de la sección
        sections = Section.objects.filter(id__in=selected_sections)
        form.sections.set(sections)

        # Agregar empleados autorizados al formulario
        authorized_employees = CustomUser.objects.filter(email__in=employee_emails)
        form.authorized_employees.set(authorized_employees)

        # Crear relaciones entre el formulario y las secciones seleccionadas
        for section in sections:
            if not FormSection.objects.filter(form=form, section=section).exists():
                FormSection.objects.create(form=form, section=section)

        # Guardar el formulario y redirigir o renderizar según sea necesario
        form.save()

        # Renderizar la plantilla HTML con los detalles del formulario creado
        return render(
            request,
            "Formulario/tempFormView.html",
            {"form": form},
        )

    # Lógica para renderizar la página de creación de formulario si no es una solicitud POST
    return render(request, "Formulario/tempCreateForm.html")


def userFormView(request):
    form_title = request.GET.get('form_title')  # Retrieve form_title from query parameters
    form = Form.objects.get(title=form_title)
    print("Form:", form)
    # Turn form into a dictionary to pass it to the template
    form = {
        "title": form.title,
        "company": form.company.companyName,
        "start_date": form.start_date,
        "end_date": form.end_date,
        "sections": form.sections.all(),
    }
    print("Form:", form)    
    options = [1, 2, 3, 4, 5]  # List of options
    
    context = {
        'form': form,
        'range_1_to_5': list(range(1, 6)),

    }
    return render(request, 'Formulario/tempUserFormView.html', {"context": context})

def submitForm(request):
    if request.method == 'POST':
        print("Se recibio un POST")
        for key, value in request.POST.items():
            if key.startswith('response_'):
                _, form_id, section_id, question_id = key.split('_')
                print(f"Form ID: {form_id}, Section ID: {section_id}, Question ID: {question_id}, Answer: {value}")
                # Uncomment the following lines to save the responses
                section = Section.objects.get(id=section_id)
                question = Question.objects.get(id=question_id)
                form = Form.objects.get(title=form_id)
                employee = CustomUser.objects.get(email=request.user.email)
                Response.objects.create(
                    employee=employee,
                    form=form,
                    section=section,
                    question=question,
                    answer=value
                )
        return redirect('Formulario:userView')

        