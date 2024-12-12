from django.contrib import admin
from .models import Employee,Cemetry,Region
# Register your models here.
class CemetryAdmin(admin.ModelAdmin):
    list_display = (['name'])
    search_fields = (['name'])

class RegionAdmin(admin.ModelAdmin):
    list_display = ('cemetry', 'region')
    search_fields = ('cemetry', 'region')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'blood_type', 'Rh_factor')

    search_fields = ('user_name', 'blood_type', 'Rh_factor')

    def user_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Cemetry, CemetryAdmin)
admin.site.register(Region, RegionAdmin)