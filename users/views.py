from rest_framework.generics import ListCreateAPIView

from users.models import Payment
from users.serializers import PaymentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


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
