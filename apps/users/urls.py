
from django.urls import path,re_path,include
from . import views

urlpatterns = [
    
    re_path(r'^vendors/', include([
        path('create-vendor',views.CreateVendorApi.as_view()),
        path('list',views.ListVendors.as_view()),
        path('update',views.EditVendorDetails.as_view()),
        path('delete',views.DeletePurchaseOrderApiView.as_view()),
        
        path('performance', views.GetVendorPerformance.as_view()),
 
    ])),
]