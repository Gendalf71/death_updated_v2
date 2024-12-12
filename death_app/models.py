from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now

# Create your models here.

# How cemetrries are stored 
class Cemetry(models.Model):

    # Cemetry has a name
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.name}"

# How regions in cemetries are stored
class Region(models.Model):

    # Region has a name of cemetry and a region 
    cemetry = models.ForeignKey(Cemetry,on_delete=models.CASCADE)
    region = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    
    def __str__(self):
        return f"{str(self.cemetry)} участок №{self.region}"

# How material of monuments are stored
class Material(models.Model):

    # Material has a name
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

class Colour(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
    
class SizeofMonument(models.Model):

    length = models.DecimalField(max_digits=10, decimal_places=0)
    width = models.DecimalField(max_digits=10, decimal_places=0)
    height = models.DecimalField(max_digits=10, decimal_places=0)
    
    class Meta:
        unique_together = ('length', 'width', 'height')

    def __str__(self):
        return f"{self.length}*{self.width}*{self.height}"

class SizeofCurbstone(models.Model):

    length = models.DecimalField(max_digits=10, decimal_places=0)
    width = models.DecimalField(max_digits=10, decimal_places=0)
    height = models.DecimalField(max_digits=10, decimal_places=0)
    
    class Meta:
        unique_together = ('length', 'width', 'height')

    def __str__(self):
        return f"{self.length}*{self.width}*{self.height}"    

class Monument(models.Model):

    name = models.CharField(max_length=100)

    material = models.OneToOneField(Material, on_delete = models.CASCADE)
    colour = models.OneToOneField(Colour, on_delete = models.CASCADE)

    size = models.OneToOneField(SizeofMonument, on_delete = models.CASCADE)
    curbstone = models.OneToOneField(SizeofCurbstone, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'material', 'colour', 'size', 'curbstone')

    def __str__(self):
        return f"{self.name} материал - {self.material}, цвет - {self.colour}, размер - {self.size}, размер тумбы - {self.curbstone}"

class Funeral(models.Model):

    name = models.CharField(max_length=100)

    date = models.DateField(default=now)  # Дата

    time = models.TimeField() # Время визита, строка в формате HH:MM

    cemetry = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='services')

    people = models.DecimalField(max_digits=10, decimal_places=0,null=True,blank=True)  
    image = models.URLField(null=True,blank=True)

    class Meta:
        unique_together = ('name', 'date', 'cemetry')

    def __str__(self):
        return f"Усопший: {self.name} вреемя похорон: {self.date}, кладбище - {self.cemetry}"

class Gravediggers(models.Model):

    name = models.CharField(max_length=100)

    start_time = models.TimeField()  # Начало рабочего дня

    end_time = models.TimeField()  # Конец рабочего дня

    def __str__(self):
        return f"{self.name}"

class Memorial(models.Model):

    name = models.CharField(max_length=100)

    location = models.CharField(max_length=255)  # Местоположение зала

    start_time = models.TimeField()  # Начало рабочего дня

    end_time = models.TimeField()  # Конец рабочего дня

    def __str__(self):
        return f"{self.name} по адресу: {self.location}"
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')  # Пользователь

    patronymic = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=255, blank=True, null=True, validators=[
        RegexValidator(r'^\+7\d{10}$', message='Номер телефона должен быть в формате +7XXXXXXXXXX')])  # Номер телефона

    email = models.EmailField()

    blood_type = models.CharField(max_length=10)  
    Rh_factor = models.CharField(max_length=10)  
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')  # Пользователь

    patronymic = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=255, blank=True, null=True, validators=[
        RegexValidator(r'^\+7\d{10}$', message='Номер телефона должен быть в формате +7XXXXXXXXXX')])  # Номер телефона

    email = models.EmailField()
    
    position = models.CharField(max_length=255)  # Должность

    blood_type = models.CharField(max_length=10)  
    Rh_factor = models.CharField(max_length=10) 

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Works(models.Model):
    work = models.CharField(max_length=100)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='visits')  # Клиент

    gravediggers = models.OneToOneField(Gravediggers, on_delete=models.CASCADE)

    date = models.DateField(default=now)  # Дата

    time = models.TimeField() # Время визита, строка в формате HH:MM

    def save(self, *args, **kwargs):
        """Метод сохранения визита и автоматического выбора зала."""
        super(Works, self).save(*args, **kwargs) # Сохраняем визит

    def __str__(self):
        return f"{self.work} {self.date} {self.time}"

class Visit(models.Model):
    memorial = models.OneToOneField(Memorial, on_delete=models.CASCADE)

    date = models.DateField(default=now)  # Дата

    time = models.TimeField() # Время визита, строка в формате HH:MM

    def __str__(self):
        return f"{self.work} {self.date} {self.time}"