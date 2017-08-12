from django.contrib import admin

from .models import Day


class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_working_day')
    # readonly_fields = ('name',)

    # def has_add_permission(self, request):
    #     return False


# Register your models here.
admin.site.register(Day, DayAdmin)
