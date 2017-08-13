from django.contrib import admin
import datetime

from .models import Day


class CurrentDayListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Current Day'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'today'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('1', 'Today'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        now = datetime.datetime.now()
        if self.value() == '1':
            return queryset.filter(name__icontains=now.strftime("%A").lower())


class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_working_day')
    list_filter = (CurrentDayListFilter, )
    icon = '<i class="material-icons">today</i>'
    # readonly_fields = ('name',)

    # def has_add_permission(self, request):
    #     return False

# Register your models here.
admin.site.register(Day, DayAdmin)
