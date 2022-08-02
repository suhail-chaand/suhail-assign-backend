from django.urls import path
from .views import (
                    session_completed_webhook,
                    CreateCheckoutSessionView,
                    )

urlpatterns = [
    path('createCheckoutSession', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('sessionCompletedWebhook', session_completed_webhook, name='checkout-session-completed'),
]
