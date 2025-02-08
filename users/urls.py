from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import PaymentListCreateView, UserRegistrationAPIView, CreatePaymentSession

app_name = "users"


urlpatterns = [
    path('payments/', PaymentListCreateView.as_view(), name='payments'),
    path('login/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('payment/', CreatePaymentSession.as_view(), name='payment')
]
