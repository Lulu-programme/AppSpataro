from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Account, Truck


@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    list_display = ('view_name', 'username', 'is_staff', 'view_truck', 'view_city')
    ordering = ('last_name',)

    @admin.display(empty_value='Truck')
    def view_truck(self, obj):
        if obj.is_staff:
            return '- Admin -'
        return obj.truck

    @admin.display(empty_value='City')
    def view_city(self, obj):
        if obj.is_superuser:
            return '- Développeur -'
        return obj.city

    @admin.display(empty_value='get_full_name')
    def view_name(self, obj):
        if obj.is_superuser:
            return 'Lulu Programmation'
        return obj.get_full_name()


@admin.register(Truck)
class TruckAdmin(ImportExportModelAdmin):
    list_display = ('license', 'technical', 'tachograph', 'adr')
    ordering = ('license',)
