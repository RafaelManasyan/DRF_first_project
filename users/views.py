from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer

from .services import create_checkout_session, create_price, create_product


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




from web_sky.models import Course

# Импорт моделей
from .models import Payment

# Предполагаем, что функции для работы со Stripe импортированы:
# from your_stripe_module import create_product, create_price, create_checkout_session

class CreatePaymentSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Используем request.data – DRF самостоятельно разбирает JSON и form-data
        data = request.data

        course_id = data.get("course_id")
        amount_value = data.get("amount")

        # Проверяем наличие необходимых данных
        if course_id is None:
            return Response({'error': 'Не указан course_id'}, status=status.HTTP_400_BAD_REQUEST)
        if amount_value is None:
            return Response({'error': 'Не указана сумма оплаты (amount)'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount_value)
        except ValueError:
            return Response({'error': 'Неверный формат суммы оплаты'}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем данные о курсе
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Шаг 1: Создаем продукт в Stripe
        product_id = create_product(course.name)
        if isinstance(product_id, dict) and product_id.get('error'):
            return Response({'error': product_id['error']}, status=status.HTTP_400_BAD_REQUEST)

        # Шаг 2: Создаем цену в Stripe (сумма в копейках)
        price_id = create_price(product_id, amount)
        if isinstance(price_id, dict) and price_id.get('error'):
            return Response({'error': price_id['error']}, status=status.HTTP_400_BAD_REQUEST)

        # Определяем URL для успешного завершения и отмены
        success_url = "http://localhost:8000/payments/success/"
        cancel_url = "http://localhost:8000/payments/cancel/"

        # Шаг 3: Создаем сессию оплаты
        session_url = create_checkout_session(price_id, success_url, cancel_url)
        if isinstance(session_url, dict) and session_url.get('error'):
            return Response({'error': session_url['error']}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем информацию о платеже
        Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            method='transfer'
        )

        return Response({'checkout_url': session_url}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        # Если GET-запрос не поддерживается, можно вернуть ошибку
        return Response({'error': 'Неверный метод запроса'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)