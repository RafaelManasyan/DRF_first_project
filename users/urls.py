from django.urls import path

from users.views import PaymentListCreateView

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListCreateView.as_view(), name="payments"),
]
