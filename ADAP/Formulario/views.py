from django.http import HttpResponse
from django.shortcuts import render
import ConexionDB as CDB # Importing db reference from ConexionDB.py
from django.http import HttpResponse


def index(request):
    """
    Index
    """
    return HttpResponse("This is an index page")

# userView view

def userView(request):
    # Retrieve email from session
    email = request.session.get('user_email')
    if email:
        # Assuming you have a function to fetch user information based on email from ConexionDB module
        user_info = CDB.get_user_info(email)
        if user_info:
            # Pass the user information to the template for rendering
            return render(request, 'Formulario/en/ViewUser.html', {'user_info': user_info})
        else:
            return HttpResponse('Error al obtener información del usuario')
    else:
        return HttpResponse('Correo no proporcionado en la sesión')