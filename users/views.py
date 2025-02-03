from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from rest_framework.filters import OrderingFilter


class PaymentListCreateView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['date']
    search_fields = ['method']

    def filter_queryset(self, queryset):
        search_param = self.request.query_params.get('search', None)
        if search_param:
            if search_param == 'course':
                try:
                    queryset = queryset.filter(course__isnull=False)
                except ValueError:
                    pass
            elif search_param == 'lesson':
                try:
                    queryset = queryset.filter(lesson__isnull=False)
                except ValueError:
                    pass
            else:
                queryset = queryset.filter(method__icontains=search_param)
        return queryset


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()