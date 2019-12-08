from django.db import models

# Create your models here.


class Sex(models.Model):
    name = models.CharField(verbose_name='nombre',
                            max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'sexo'
        verbose_name_plural = 'sexos'

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(verbose_name='nombre',
                            max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'posición'
        verbose_name_plural = 'posiciones'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(verbose_name='nombre',
                            max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamento'

    def __str__(self):
        return self.name


class Employee(models.Model):
    id_document = models.CharField(
        verbose_name='documento de identidad', max_length=30, null=False, blank=False, unique=True)
    first_name = models.CharField(
        verbose_name='nombres', max_length=60, null=False, blank=False)
    last_name = models.CharField(
        verbose_name='apellidos', max_length=60, null=False, blank=False)
    sex = models.ForeignKey(
        to=Sex, on_delete=models.CASCADE, verbose_name='sexo')
    birth_date = models.DateField(
        verbose_name='fecha de nacimiento', null=False, blank=False)

    department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, verbose_name='departamento')
    position = models.ForeignKey(
        to=Position, on_delete=models.CASCADE, verbose_name='posición')

    monthly_salary = models.DecimalField(
        verbose_name='salario mensual', max_digits=14, decimal_places=4, null=False, blank=False)

    active = models.BooleanField(verbose_name='activo', default=True)

    created_at = models.DateTimeField(
        verbose_name='fecha de creación', auto_now_add=True)
    modified_at = models.DateTimeField(
        verbose_name='fecha de modificación', auto_now=True)

    class Meta:
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'

    def age(self):
        from datetime import date
        return date.today().year - self.birth_date.year - ((date.today().month, date.today().day) < (self.birth_date.month, self.birth_date.day)) if self.birth_date else None

    def hourly_salary(self):
        return self.monthly_salary / 52

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else self.first_name if self.first_name else None
