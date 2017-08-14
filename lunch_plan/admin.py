from django.contrib import admin

from work_week.models import Day
from .models import DailyPlan, WeeklyPlan


class DailyPlanAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">restaurant</i>'
    exclude = []
    list_display = []
    
    def changelist_view(self, request, extra_context=None):
        self.list_display = []
        if not request.user.is_superuser:
            self.list_display = ['date', 'day', 'will_have_lunch']
        else:
            self.list_display = ['date', 'day', 'user', 'will_have_lunch']
        return super(DailyPlanAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(DailyPlanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.extend(['user', ])
        return super(DailyPlanAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()


class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = []
    icon = '<i class="material-icons">shopping_cart</i>'
    exclude = []

    def changelist_view(self, request, extra_context=None):
        self.list_display = []
        if not request.user.is_superuser:
            self.list_display = ['admin_names']
        else:
            self.list_display = ['user', 'admin_names']
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

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.extend(['user', ])
        return super(WeeklyPlanAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

# Register your models here.
admin.site.register(DailyPlan, DailyPlanAdmin)
admin.site.register(WeeklyPlan, WeeklyPlanAdmin)
