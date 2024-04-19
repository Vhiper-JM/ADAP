from django.shortcuts import render
import ConexionDB as CDB # Importing db reference from ConexionDB.py



def index(request):
    """
    Muestra el inicio de la plataforma con el login en ingles
    """
    return render(request, "Formulario/en/ViewUser.html")