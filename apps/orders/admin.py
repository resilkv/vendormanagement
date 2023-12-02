from django.contrib import admin

from apps.orders.models import PurchaseOrder

# Register your models here.
admin.site.register(PurchaseOrder)