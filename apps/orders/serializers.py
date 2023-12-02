from rest_framework import serializers
from django.utils import timezone
from apps.orders.models import HistoricalPerformance, PurchaseOrder
from apps.users.models import Vendor
from django.db.models import F
from django.db.models import Avg

class CreateorUpdatePurchaseOrderSerializer(serializers.ModelSerializer):
    
    po_id = serializers.PrimaryKeyRelatedField(queryset=PurchaseOrder.objects.all(),required=False)
    vendor_id = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(),required=False,default=None)
    order_date = serializers.CharField(required=False)
    items = serializers.JSONField(required=False)
    quantity = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    quality_rating = serializers.FloatField(required=False)
    issue_date = serializers.DateTimeField(required=False)
    delivery_date = serializers.CharField(required=False)
    has_issue = serializers.BooleanField(default=False)
    
    class Meta:
        model = PurchaseOrder
        fields= ['po_id','vendor_id','po_number','vendor_id','order_date','items','quantity','status','issue_date',
                 'quality_rating','delivery_date','has_issue']
        
    extra_kwargs = {
        'po_id': {'help_text': 'Only when editing a Purchase Order'},
        'vendor_id': {'help_text': 'Enter Vendor ID'},
        'status': {'help_text': 'Status of the Purchase Order', 'choices': ['pending', 'completed', 'cancelled']}
    } 
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        instance = PurchaseOrder()
        instance.vendor = validated_data.get('vendor_id')
        instance.po_number = validated_data.get('po_number')
        instance.order_date = validated_data.get('order_date')
        instance.items = validated_data.get('items')
        instance.quantity = validated_data.get('quantity')
        instance.status = validated_data.get('status')
        instance.issue_date = validated_data.get('issue_date')
        instance.save()
        return instance 
    
    def update(self, instance, validated_data):
        
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        instance.has_issue = validated_data.get('has_issue',False)
        if validated_data.get('status') == 'completed':
            
            instance.completed_date = timezone.now()
            instance.quality_rating = validated_data.get('quality_rating',None)
            instance.save()
            total_po_count = PurchaseOrder.objects.filter(vendor=instance.vendor, completed_date__lte=F('delivery_date')).count()
            total_po = PurchaseOrder.objects.filter(vendor=instance.vendor,status='completed').count()
           
            historical_performance = HistoricalPerformance.objects.get(vendor=instance.vendor)

            
            historical_performance.on_time_delivery_rate = total_po_count/total_po
            if validated_data.get('quality_rating',None) is not None:
                average_quality_rating = PurchaseOrder.objects.values('vendor').annotate(avg_quality_rating=Avg('quality_rating'))
                result_for_specific_vendor = average_quality_rating.filter(vendor=instance.vendor).order_by('vendor').first()
                avg_quality_rating_for_specific_vendor = result_for_specific_vendor.get('avg_quality_rating', 0.0)
                historical_performance.quality_rating_avg = avg_quality_rating_for_specific_vendor
            
            total_fullfilment_with_issue = PurchaseOrder.objects.filter(vendor=instance.vendor,status='completed',has_issues=True).count()
            
            historical_performance.fulfillment_rate = total_fullfilment_with_issue/total_po
            
            historical_performance.save()
        instance.save()

        return instance
    
class DeletePurchaseOrderSerializer(serializers.ModelSerializer):

    po_id = serializers.PrimaryKeyRelatedField(queryset=PurchaseOrder.objects.all())

    class Meta:
        model =  PurchaseOrder
        fields = ['po_id']   
 
    def validate(self, attrs):
        return super().validate(attrs)        

class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    
    po_id = serializers.PrimaryKeyRelatedField(queryset =PurchaseOrder.objects.all() )
    
    class Meta:
        model =  PurchaseOrder
        fields = ['po_id']   
 
    def update(self, instance, validated_data):
        instance.acknowledgment_date = timezone.now()
        instance.save()
        if instance.issue_date and instance.acknowledgment_date:
            time_difference = (instance.acknowledgment_date - instance.issue_date).total_seconds()
            historical_performance = HistoricalPerformance.objects.get(vendor=instance.vendor)
            historical_performance.average_response_time = time_difference
            historical_performance.save()
      
        return instance
    
 