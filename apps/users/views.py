from django.shortcuts import render
from rest_framework import generics
from apps.orders.models import HistoricalPerformance
from apps.users.models import Vendor
from apps.users.schemas import VendorListingSchema, VendorPerformanceSchema
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

class CreateVendorApi(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateVendorApi, self).__init__(**kwargs)

    serializer_class = CreateorUpdateCreateVendorSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Vendor"])
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
        



class ListVendors(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ListVendors, self).__init__(**kwargs)

    queryset = Vendor.objects.filter().order_by('-id')
    serializer_class = VendorListingSchema
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['']

    vendor_id = openapi.Parameter('vendor_id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter Vendor id")
    

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Vendor"], manual_parameters=[vendor_id])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('vendor_id', None)
     
        if instance_id :
            queryset = queryset.filter(pk=instance_id)

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)       
    


class EditVendorDetails(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(EditVendorDetails, self).__init__(**kwargs)

    serializer_class = CreateorUpdateCreateVendorSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Vendor"])
    def put(self, request):
        try:
            serializer = self .serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.validated_data.get('vendor_id',None)
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

    serializer_class = DeleteVendorsSerializer
    # permission_classes = (IsAuthenticated,)

   
    @swagger_auto_schema(tags=["Vendor"], request_body=serializer_class)
    def delete(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context = {'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            instance = serializer.validated_data.get('vendor_id')
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




class GetVendorPerformance(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetVendorPerformance, self).__init__(**kwargs)

    queryset = HistoricalPerformance.objects.filter().order_by('-id')
    serializer_class = VendorPerformanceSchema
    pagination_class = RestPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['']

    vendor_id = openapi.Parameter('vendor_id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter Vendor id")
    

    @swagger_auto_schema(pagination_class=RestPagination, tags=["Vendor Performace"], manual_parameters=[vendor_id])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('vendor_id', None)
        queryset = queryset.filter(pk=instance_id)

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True,context={'request': request})
        return self.get_paginated_response(serializer.data)    