from rest_framework import serializers
from apps.orders.models import HistoricalPerformance

from apps.users.models import Vendor


class CreateorUpdateCreateVendorSerializer(serializers.ModelSerializer):
    
    vendor_id = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(),required=False)
    name = serializers.CharField(required=False)
    contact_details = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    vendor_code = serializers.CharField(required=False)
    
    class Meta:
        model = Vendor
        fields= ['vendor_id','name','contact_details','address','vendor_code']
        
    extra_kwargs = {
        'vendor_id': {'help_text': 'Only when editing a vendor'},
    }    
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        instance = Vendor()
        instance.name = validated_data.get('name')
        instance.contact_details = validated_data.get('contact_details')
        instance.address = validated_data.get('address')
        instance.vendor_code = validated_data.get('vendor_code')
        instance.save()
        HistoricalPerformance(vendor=instance).save()
        return instance  
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class DeleteVendorsSerializer(serializers.ModelSerializer):

    vendor_id = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model =  Vendor
        fields = ['vendor_id']   
 
    def validate(self, attrs):
        return super().validate(attrs)    