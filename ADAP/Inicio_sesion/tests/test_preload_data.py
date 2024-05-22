from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

class PreloadDataTestCase(TestCase):
    def setUp(self):
        # Datos de prueba para las compañías
        self.company_data_1 = {
            'companyName': "Company Test 1",
            'dateFoundation': timezone.now().date(),
            'email': "company1@test.com",
            'NIT': "1234567890",
            'phone': "1234567890",
            'password': "company1password",
            'country': "Testland",
        }

        self.company_data_2 = {
            'companyName': "Company Test 2",
            'dateFoundation': timezone.now().date(),
            'email': "company2@test.com",
            'NIT': "0987654321",
            'phone': "0987654321",
            'password': "company2password",
            'country': "Testlandia",
        }

        # Datos de prueba para los empleados
        self.user_data_1 = {
            'name': "John",
            'surname': "Doe",
            'id': "ID12345",
            'gender': "M",
            'nationality': "Testland",
            'phone': "1234567890",
            'country': "Testland",
            'birthdate': "1990-01-01",
            'email': "john.doe@company1.com",
            'company': "Company Test 1",
            'position': "Developer",
            'isEntrepreneur': False,
            'entrepreneurship': "",
            'password': "johndoepassword"
        }

        self.user_data_2 = {
            'name': "Jane",
            'surname': "Smith",
            'id': "ID54321",
            'gender': "F",
            'nationality': "Testland",
            'phone': "0987654321",
            'country': "Testland",
            'birthdate': "1992-02-02",
            'email': "jane.smith@company1.com",
            'company': "Company Test 1",
            'position': "Manager",
            'isEntrepreneur': False,
            'entrepreneurship': "",
            'password': "janesmithpassword"
        }

        self.user_data_3 = {
            'name': "Alice",
            'surname': "Johnson",
            'id': "ID67890",
            'gender': "F",
            'nationality': "Testlandia",
            'phone': "1231231234",
            'country': "Testlandia",
            'birthdate': "1995-03-03",
            'email': "alice.johnson@company2.com",
            'company': "Company Test 2",
            'position': "Analyst",
            'isEntrepreneur': False,
            'entrepreneurship': "",
            'password': "alicejohnsonpassword"
        }

        self.user_data_4 = {
            'name': "Bob",
            'surname': "Brown",
            'id': "ID09876",
            'gender': "M",
            'nationality': "Testlandia",
            'phone': "4321432143",
            'country': "Testlandia",
            'birthdate': "1997-04-04",
            'email': "bob.brown@company2.com",
            'company': "Company Test 2",
            'position': "Tester",
            'isEntrepreneur': False,
            'entrepreneurship': "",
            'password': "bobbrownpassword"
        }

    def test_create_companies_and_users(self):
        # Crear compañía 1
        response = self.client.post(reverse('Inicio_sesion:signup_business'), data=self.company_data_1)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro

        # Crear compañía 2
        response = self.client.post(reverse('Inicio_sesion:signup_business'), data=self.company_data_2)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro

        # Crear usuarios
        response = self.client.post(reverse('Inicio_sesion:signup'), data=self.user_data_1)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro

        response = self.client.post(reverse('Inicio_sesion:signup'), data=self.user_data_2)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro

        response = self.client.post(reverse('Inicio_sesion:signup'), data=self.user_data_3)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro

        response = self.client.post(reverse('Inicio_sesion:signup'), data=self.user_data_4)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro

    @classmethod
    def tearDownClass(cls):
        # Sobrescribe tearDownClass para evitar que los datos de prueba se eliminen
        pass
