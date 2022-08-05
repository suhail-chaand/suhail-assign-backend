from django.urls import path
from .views import (ProductView,
                    AddProductView)

urlpatterns = [
    path('addProduct', AddProductView.as_view(), name='add-product'),
    path('getProduct/<int:pk>/', ProductView.as_view(), name='get-product'),
]
