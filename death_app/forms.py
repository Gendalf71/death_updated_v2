from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Client, Employee, Funeral, Cemetry, Region, Gravediggers, Works
from datetime import datetime, timedelta
from .time_slots import get_time_slots

# Форма регистрации клиента
class ClientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

# Форма для регистрации клиента
class ClientForm(forms.ModelForm):

    BLOOD_TYPE_CHOICES = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    )

    RH_FACTOR_CHOICES = (
        ('+', '+'),
        ('-', '-'),
    )

    username = forms.CharField(label='Логин', max_length=150)
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150)

    patronymic = forms.CharField(required=False, label='Отчество', max_length=150)

    phone_number = forms.CharField(label='Номер телефона', max_length=150)
    email = forms.EmailField(required=True)

    blood_type = forms.CharField(label='Группа крови', widget=forms.Select(choices=BLOOD_TYPE_CHOICES))
    Rh_factor = forms.CharField(label='Резус-фактор', widget=forms.Select(choices=RH_FACTOR_CHOICES))

    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'blood_type', 'Rh_factor']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество', 
            'phone_number': 'Номер телефона', 
            'email': 'email', 
            'blood_type': 'Группа крови', 
            'Rh_factor': 'Резус-фактор'
        }

# Форма регистрации сотрудника
class EmployeeRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

# Форма для добавления/редактирования данных сотрудника
class EmployeeForm(forms.ModelForm):

    BLOOD_TYPE_CHOICES = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    )

    RH_FACTOR_CHOICES = (
        ('+', '+'),
        ('-', '-'),
    )

    username = forms.CharField(label='Логин', max_length=150)
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150)

    patronymic = forms.CharField(required=False, label='Отчество', max_length=150)

    phone_number = forms.CharField(label='Номер телефона', max_length=150)
    email = forms.EmailField(required=True)

    position = forms.CharField(label='Должность')

    blood_type = forms.CharField(label='Группа крови', widget=forms.Select(choices=BLOOD_TYPE_CHOICES))
    Rh_factor = forms.CharField(label='Резус-фактор', widget=forms.Select(choices=RH_FACTOR_CHOICES))
    
    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'position', 'blood_type', 'Rh_factor']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество', 
            'phone_number': 'Номер телефона', 
            'email': 'email', 
            'position': 'Должность',
            'blood_type': 'Группа крови', 
            'Rh_factor': 'Резус-фактор'
        }

class CemetryForm(forms.ModelForm):
    class Meta:
        model = Cemetry
        fields = ['name']
        labels = {
            'name': 'Название кладбища',
        }

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['cemetry','region']
        labels = {
            'cemetry': 'Кладбища',
            'region': 'Номер участка',
        }

class FuneralForm(forms.ModelForm):

    date = forms.DateField(label='Дата  посещения',
                           widget=forms.DateInput(
                               attrs={'type': 'date', 'id': 'id_date', 'min': datetime.today().strftime('%Y-%m-%d'),

                                      'max': (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')}))

    time = forms.TimeField(label='Время посещения',widget=forms.TimeInput(attrs={'type': 'time'}, format='%H'))

    class Meta:
        model = Funeral
        fields = ['name', 'date', 'time', 'cemetry', 'people', 'image']
        labels = {
            'name': 'Фио усопшего',
            'date': 'время похорон',
            'time': 'время похорон',
            'cemetry': 'Участок на кладбище',
            'people': 'Число присутствоваших',
            'image': 'Фото с похорон',
        }

        cemetry = forms.ModelChoiceField(queryset=Region.objects.all())

class GravediggersForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Название бригады', )

    start_time = forms.TimeField(label='Начало работы зала',
                                 widget=forms.TimeInput(attrs={'type': 'time'}, format='%H'))

    end_time = forms.TimeField(label='Конец работы зала',
                               widget=forms.TimeInput(attrs={'type': 'time'}, format='%H'))
    
    class Meta:
        model = Gravediggers
        fields = ['name', 'start_time', 'end_time']
        labels = {
            'name': 'Название бригады',
            'start_time': 'Начало работы зала',
            'end_time': 'Конец работы зала',
        }

class WorksForm(forms.ModelForm):

    works_choices = (
        ('Похороны', 'Похороны'),
    )
    work = forms.CharField(label='Работы', widget=forms.Select(choices=works_choices))

    date = forms.DateField(label='Дата  посещения',
                           widget=forms.DateInput(
                               attrs={'type': 'date', 'id': 'id_date', 'min': datetime.today().strftime('%Y-%m-%d'),

                                      'max': (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')}))

    time = forms.TimeField(label='Время посещения',widget=forms.TimeInput(attrs={'type': 'time'}, format='%H'))

    class Meta:
        model = Works
        fields = ['work', 'gravediggers', 'date','time']
        labels = {
            'work': 'Название бригады',
            'gravediggers': 'Начало работы зала',
            'date': 'Конец работы зала',
            'time': 'Конец работы зала',
        }

        gravediggers = forms.ModelChoiceField(queryset=Gravediggers.objects.all())

    def __init__(self, *args, **kwargs):  # args - список аргументов, kwargs - словарь аргументов
        super(WorksForm, self).__init__(*args, **kwargs)

        # Добавим доступные слоты времени в поле time
        if 'gravediggers' in self.data and 'date' in self.data:
            employee_id = self.data.get('gravediggers')
            date_id = self.data.get('date')

            gravediggers = Gravediggers.objects.get(id=employee_id)
            date = datetime.strptime(date_id, '%Y-%m-%d').date()

            available_time = get_time_slots(gravediggers, date)

            # Преобразуем список доступных временных слотов в choices для поля
            self.fields['time'].choices = [(slot, slot) for slot in available_time]
