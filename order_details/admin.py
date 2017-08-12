from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'day')
    actions = ['generate_order']

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('date', 'day', 'no_of_orders')
        return super(OrderAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__in=[request.user])

    
    def generate_shipping_partner(self, request, queryset):


# Register your models here.
admin.site.register(Order, OrderAdmin)
