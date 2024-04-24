from django.db import models

# Agregar NIT a la clase
class Company(models.Model):
    companyName = models.CharField(max_length=100)
    foundationDate = models.DateField()
    email = models.EmailField(unique=True)
    NIT = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Consider hashing passwords


class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identification = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    nationality = models.CharField(max_length=100)
    country_residence = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    is_entrepreneur = models.BooleanField(default=False)
    entrepreneurship_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
