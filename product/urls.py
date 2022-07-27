from django.urls import path
from .views import ProductView

urlpatterns = [
    path('getProduct/<int:pk>/', ProductView.as_view(), name='get-product')
]
