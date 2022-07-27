from django.urls import (path,
                         include
                         )
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="MB - Final Assignment",
      default_version='v1',
   ),
)

urlpatterns = [
    path('product/', include('product.urls')),

    path('admin', admin.site.urls),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
