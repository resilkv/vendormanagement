from django.db import models
from apps.users.models import Vendor
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Count, Avg

ORDER_STATUS_CHOICES = (
    ('pending', _('Pending')),
    ('completed', _('Completed')),
    ('cancelled', _('Cancelled'))
)

class PurchaseOrder(models.Model):
    
    po_number = models.CharField(unique=True, max_length=255, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20,default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    has_issues = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.pk)
    
   
    
class HistoricalPerformance(models.Model):
    
    vendor = models.ForeignKey(Vendor,null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)