from django.shortcuts import render

from django.shortcuts import render
from rest_framework import generics
from apps.orders.models import PurchaseOrder
from apps.orders.schemas import ListPuchaseOrder
from apps.orders.serializers import CreateorUpdatePurchaseOrderSerializer, DeletePurchaseOrderSerializer, PurchaseOrderAcknowledgeSerializer
from apps.users.models import Vendor
from apps.users.schemas import VendorListingSchema
from apps.users.serializers import CreateorUpdateCreateVendorSerializer, DeleteVendorsSerializer
from vendormanagement.helpers.pagination import RestPagination
from vendormanagement.helpers.response import ResponseInfo
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
# Create your views here.

class CreatePurchaseOrder(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreatePurchaseOrder, self).__init__(**kwargs)

    serializer_class = CreateorUpdatePurchaseOrderSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Purchase Order"])
    def post(self, request):
        try:

            serializer = self.serializer_class(
                data=request.data, context={'request': request})

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = "_success"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class ListPurchaseOrder(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ListPurchaseOrder, self).__init__(**kwargs)

    queryset = PurchaseOrder.objects.filter().order_by('-id')
    serializer_class = ListPuchaseOrder
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['']

    po_id = openapi.Parameter('po_id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter Purchase Order id")
    

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Purchase Order"], manual_parameters=[po_id])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('po_id', None)
     
        if instance_id :
            queryset = queryset.filter(pk=instance_id)

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)       
    


class EditPuchaseOrderDetails(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(EditPuchaseOrderDetails, self).__init__(**kwargs)

    serializer_class = CreateorUpdatePurchaseOrderSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Purchase Order"])
    def put(self, request):
        try:
            
            serializer = self .serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.validated_data.get('po_id',None)
            serializer = self.serializer_class(
                    instance, data=request.data, context={'request': request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = "_success"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeletePurchaseOrderApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeletePurchaseOrderApiView, self).__init__(**kwargs)

    serializer_class = DeletePurchaseOrderSerializer
    # permission_classes = (IsAuthenticated,)

   
    @swagger_auto_schema(tags=["Purchase Order"], request_body=serializer_class)
    def delete(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context = {'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            instance = serializer.validated_data.get('po_id')
            instance.delete()
           

            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["message"] = "_success"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
           
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
        
class PurchaseOrderAcknowledgeApi(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(PurchaseOrderAcknowledgeApi, self).__init__(**kwargs)

    serializer_class = PurchaseOrderAcknowledgeSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Purchase Order Acknowledge"])
    def put(self, request):
        try:
            
            serializer = self .serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.validated_data.get('po_id',None)
            serializer = self.serializer_class(
                    instance, data=request.data, context={'request': request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = "_success"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        