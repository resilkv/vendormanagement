

from django.urls import path,re_path,include
from . import views

urlpatterns = [
    
    re_path(r'^purchse_orders/', include([
        path('create',views.CreatePurchaseOrder.as_view()),
        path('list',views.ListPurchaseOrder.as_view()),
        path('update',views.EditPuchaseOrderDetails.as_view()),
        path('delete',views.DeletePurchaseOrderApiView.as_view()),
        path('acknowledge', views.PurchaseOrderAcknowledgeApi.as_view(), name='acknowledge'),

    ])),
]