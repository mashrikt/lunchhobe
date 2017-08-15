from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'day', 'no_of_orders')
    readonly_fields = ('day',)
    icon = '<i class="material-icons">receipt</i>'

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('date', 'day')
        return super(OrderAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__in=[request.user])


# Register your models here.
admin.site.register(Order, OrderAdmin)
