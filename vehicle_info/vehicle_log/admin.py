from django.contrib import admin
from .models import VehicleLog
from rutedata.models import Line
# Register your models here.


class LogAdmin(admin.ModelAdmin):
    list_display = ('line_ref', 'operator_ref', 'vehicle_ref', 'vehicle_type', 'origin_departure_time')
    list_filter = ('origin_departure_time', 'line_ref', 'operator_ref', 'vehicle_ref')
    readonly_fields = ['vehicle_type', 'origin', 'destination']


admin.site.register(VehicleLog, LogAdmin)


class VehiclesInline(admin.TabularInline):
    model = VehicleLog
    fields = ['vehicle_ref', 'origin_departure_time', 'operator_ref']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class LineAdmin(admin.ModelAdmin):
    # readonly_fields = ['vehicles']
    inlines = [VehiclesInline]


admin.site.unregister(Line)
admin.site.register(Line, LineAdmin)
