from django.contrib import admin

from apps.order.models import Order, OrderFood

admin.site.register(Order)
admin.site.register(OrderFood)