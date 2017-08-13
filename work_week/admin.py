from django.contrib import admin
import datetime

from django.contrib.auth.models import User

from lunch_plan.models import WeeklyPlan
from order_details.models import Order
from .models import Day


class CurrentDayListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Current Day'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'today'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Today'),
        )

    def queryset(self, request, queryset):
        now = datetime.datetime.now()
        if self.value() == '1':
            return queryset.filter(name__icontains=now.strftime("%A"))


class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_working_day')
    list_filter = (CurrentDayListFilter, )
    actions = ['generate_order']
    icon = '<i class="material-icons">today</i>'

    def generate_order(self, request, queryset):
        # get the current day from the working day table
        current_day = queryset.values_list('name', flat=True).all()[0]
        # print(current_day)
        # find users who have subscribed for lunch for today
        total = 0
        order = Order.objects.create(day=Day.objects.get(name=current_day), date=datetime.datetime.today())
        user_id_list = []
        for plan in (WeeklyPlan.objects.values_list('user', flat=True)
                               .filter(office_lunch_days__name__icontains=current_day)):
            # print(User.objects.get(id=plan))
            total += order.price
            user_id_list.append(plan)

        order.user = user_id_list
        order.total = total
        order.menu = "Surprise Niggas!"
        order.save()

    generate_order.short_description = "Generate today's order in order table"

    # readonly_fields = ('name',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Day, DayAdmin)
