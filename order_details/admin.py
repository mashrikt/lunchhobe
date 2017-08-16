from datetime import datetime
from django import forms
from django.contrib import admin
from django.utils import timezone
from django.contrib.admin.helpers import ActionForm

from lunch_plan.models import WeeklyPlan, DailyPlan
from order_details.config import DateWeekDay
from work_week.models import Day
from .models import Order


def create_order(modeladmin, request, queryset):
    date = request.POST['date']
    date = datetime.strptime(date, '%Y-%m-%d')
    current_day = DateWeekDay.CHOICES[date.weekday()][1]
    total = 0
    order = Order.objects.create(day=Day.objects.get(name=current_day), date=date)
    user_id_set = set()
    for user in (WeeklyPlan.objects.values_list('user', flat=True)
                         .filter(office_lunch_days__name__icontains=current_day)):
        user_id_set.add(user)

    for plan in (DailyPlan.objects.values_list('user', flat=True).filter(date__exact=date)):
        user_id_set.add(plan)

    for plan in (DailyPlan.objects.values_list('user', flat=True)
                         .filter(date__exact=date, will_have_lunch=False)):
        user_id_set.remove(plan)

    for ids in user_id_set:
        total += order.price

    order.user = user_id_set
    order.total = total
    order.menu = "Surprise Niggas!"
    order.save()
    modeladmin.message_user(request, f"Order created for {date}, {current_day}")
    create_order.short_description = 'Create Order'


def view_order(modeladmin, request, queryset):
    date = request.POST['date']
    date = datetime.strptime(date, '%Y-%m-%d')
    current_day = DateWeekDay.CHOICES[date.weekday()][1]
    user_id_set = set()
    
    for user in (WeeklyPlan.objects.values_list('user', flat=True)
                         .filter(office_lunch_days__name__icontains=current_day)):
        user_id_set.add(user)

    for plan in (DailyPlan.objects.values_list('user', flat=True).filter(date__exact=date)):
        user_id_set.add(plan)

    for plan in (DailyPlan.objects.values_list('user', flat=True)
                         .filter(date__exact=date, will_have_lunch=False)):
        user_id_set.remove(plan)

    print(user_id_set)
    modeladmin.message_user(request, f"For {date}, {current_day} there is {len(user_id_set)} orders")
    view_order.short_description = 'View Order'


class GenerateOrderActionForm(ActionForm):
    date = forms.DateField(initial=timezone.now)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'day_of_week', 'no_of_orders', 'total']
    readonly_fields = ('total',)
    icon = '<i class="material-icons">receipt</i>'
    action_form = GenerateOrderActionForm
    actions = [create_order, view_order]

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ['date', 'day_of_week']

        if 'action' in request.POST and (request.POST['action'] == 'create_order'
                                         or request.POST['action'] == 'view_order'):
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Order.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(OrderAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__in=[request.user])

# Register your models here.
admin.site.register(Order, OrderAdmin)
