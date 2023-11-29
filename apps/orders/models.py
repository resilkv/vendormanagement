from django.db import models
from apps.users.models import Vendor
from django.utils.translation import gettext_lazy as _


ORDER_STATUS_CHOICES = (
    ('pending', _('Pending')),
    ('completed', _('Completed')),
    ('cancelled', _('Cancelled'))
)

class PurchaseOrder(models.Model):
    
    po_number = models.CharField(unique=True, max_length=255, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField()

    def __str__(self):
        return str(self.pk)
    
    
class HistoricalPerformance(models.Model):
    
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return str(self.pk)