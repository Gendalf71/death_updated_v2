from datetime import timedelta, datetime
from .models import Works, Gravediggers
from django.db.models import Q


# Функция для генерации временных слотов
def get_time_slots(gravediggers, date):
    start_time = gravediggers.start_time  # Начало работы
    end_time = gravediggers.end_time  # Конец работы

    # Длительность услуги
    works_duration = 120  # В минутах

    # Все записи для данного зала на указанную дату
    existing_works = Works.objects.filter(gravediggers =gravediggers, date=date)

    # Создание занятых временных слотов
    occupied_time_slots = []

    for visit in existing_works:

        # Проверка типа данных приходящего из класса времени, если строка то преобразуем в тип данных datetime
        if isinstance(visit.time, str):
            time = datetime.strptime(visit.time, '%H:%M:%S').time()
        else:
            time = visit.time

        visit_start_time = datetime.combine(date, time)  # Время начала визита
        visit_end_time = visit_start_time + timedelta(minutes=works_duration)  # Время окончания визита

        # Добавление занятых временных слотов
        occupied_time_slots.append((visit_start_time, visit_end_time))

    # Генерация свободных временных слотов
    available_time_slots = []

    current_time_temp = datetime.combine(date, start_time)  # Текущее время (datetime)

    while current_time_temp.time() < end_time and current_time_temp.time() not in occupied_time_slots:  # Пока текущее время меньше конечного времени
        slot_start = current_time_temp  # Начало временного слота
        slot_end = slot_start + timedelta(minutes=works_duration)  # Конец временного слота

        # Проверяем, пересекается ли этот слот с занятыми
        if not any(oc_start < slot_end and slot_start < oc_end for oc_start, oc_end in occupied_time_slots):
            available_time_slots.append(slot_start.time().strftime('%H:%M'))

        # Шаг между выбором времени по умолчанию - 1 час
        current_time_temp += timedelta(minutes=works_duration)

    return available_time_slots


# Функция для обновления статусов визитов
def update_status_visits():
    date, time = datetime.now().date(), datetime.now().time()  # Текущая дата и время

    # Получаем статусы визитов и обновляем их. Если дата визита равна текущей, но время визита меньше или равно текущему времени
    Works.objects.filter(
        (Q(date__lt=date) | Q(date=date, time__lt=time.strftime('%H:%M'))) & Q(status='Запланирована')).update(
        status='Выполнена')
