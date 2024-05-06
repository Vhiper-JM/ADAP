from django.db import models
from Inicio_sesion.models import CustomUser, Company

# Create your models here.

class Form(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    authorized_employees = models.ManyToManyField(CustomUser, through='FormEmployeeAssignment')

    def __str__(self):
        return self.title

class Section(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    statement = models.TextField()

    def __str__(self):
        return self.statement

class FormEmployeeAssignment(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.form.title} - {self.employee.first_name} {self.employee.last_name}"

