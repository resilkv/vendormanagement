from rest_framework import serializers
from apps.orders.models import HistoricalPerformance

from apps.users.models import Vendor


class VendorListingSchema(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields = ['id','name','contact_details','address','vendor_code','on_time_delivery_rate','quality_rating_avg','fulfillment_rate'
                ,'average_response_time']
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

class VendorPerformanceSchema(serializers.ModelSerializer):
    
    class Meta:
        model = HistoricalPerformance
        fields = ['on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas