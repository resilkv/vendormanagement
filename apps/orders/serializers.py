from rest_framework import serializers
from django.utils import timezone
from apps.orders.models import HistoricalPerformance, PurchaseOrder
from apps.users.models import Vendor


class CreateorUpdatePurchaseOrderSerializer(serializers.ModelSerializer):
    
    po_id = serializers.PrimaryKeyRelatedField(queryset=PurchaseOrder.objects.all(),required=False)
    vendor_id = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(),required=False,default=None)
    order_date = serializers.CharField(required=False)
    items = serializers.JSONField(required=False)
    quantity = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    quality_rating = serializers.FloatField(required=False)
    issue_date = serializers.DateTimeField(required=False)
    
    class Meta:
        model = PurchaseOrder
        fields= ['po_id','vendor_id','po_number','vendor_id','order_date','items','quantity','status','issue_date','quality_rating']
        
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
        
        old_status = instance.status 
        instance.vendor = validated_data.get('vendor_id', instance.vendor)
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        if validated_data.get('status') == 'completed':
            
            instance.delivery_date = timezone.now()
            instance.quality_rating = validated_data.get('quality_rating','')
     
        instance.save()
        
        if old_status != instance.status:
            self.update_fulfillment_rate(instance.vendor)

        return instance
    
    @staticmethod
    def update_fulfillment_rate(vendor):
        total_po_count = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_po_count = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            has_issues=False  
        ).count()

        fulfillment_rate = 0.0
        if total_po_count > 0:
            fulfillment_rate = fulfilled_po_count / total_po_count

        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={'fulfillment_rate': fulfillment_rate}
        )
    
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
      
            self.update_average_response_time(instance.vendor, time_difference)
        return instance
    
    @staticmethod
    def update_average_response_time(vendor, time_difference):
      
        current_average_response_time = HistoricalPerformance.objects.filter(
            vendor=vendor,
            date=timezone.now()
        ).values('average_response_time').first()
        
        if not current_average_response_time:
            HistoricalPerformance.objects.create(
                vendor=vendor,
                date=timezone.now(),
                average_response_time=time_difference
            )
        else:
            total_time = current_average_response_time['average_response_time'] + time_difference
            total_orders = PurchaseOrder.objects.filter(
                vendor=vendor,
                status='completed',
                acknowledgment_date__isnull=False
            ).count()

            new_average_response_time = total_time / total_orders
            
        HistoricalPerformance.objects.filter(vendor=vendor,date=timezone.now()).update(average_response_time=new_average_response_time)