from django.contrib import admin

from work_week.models import Day
from .models import DailyPlan, WeeklyPlan


class DailyPlanAdmin(admin.ModelAdmin):
    list_display = ('day', 'date', 'will_have_lunch')
    icon = '<i class="material-icons">restaurant</i>'

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('user', 'day', 'date', 'will_have_lunch')
        return super(DailyPlanAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(DailyPlanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ('admin_names',)
    icon = '<i class="material-icons">shopping_basket</i>'

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('user', 'admin_names')
        return super(WeeklyPlanAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(WeeklyPlanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "office_lunch_days":
            kwargs["queryset"] = Day.objects.filter(is_working_day=True)
        return super(WeeklyPlanAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

# Register your models here.
admin.site.register(DailyPlan, DailyPlanAdmin)
admin.site.register(WeeklyPlan, WeeklyPlanAdmin)
