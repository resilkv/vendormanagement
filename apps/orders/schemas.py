from rest_framework import serializers

from apps.orders.models import PurchaseOrder

class ListPuchaseOrder(serializers.ModelSerializer):
    
    vendor_name = serializers.CharField(source='vendor.name',allow_null=True)
    
    class Meta:
        model = PurchaseOrder
        fields = ['id','po_number','vendor_id','vendor_name','order_date','delivery_date',
                  'items','quantity','status','quality_rating','issue_date','acknowledgment_date']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    