from django.contrib import admin
from django.urls import path,re_path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView
from django.conf.urls.static import static
from vendormanagement import settings


schema_view = get_schema_view(
   openapi.Info(
      title="Vendor Management API",
      default_version='v1',
      description="",
      terms_of_service="",
      contact=openapi.Contact(email="resilradhakrishnan@gmail.com"),    
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    re_path(r'^api/', include('apps.users.urls')),
    re_path(r'^api/', include('apps.orders.urls')),
    re_path(r'^docs/', include([
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
            

        ])),    
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
