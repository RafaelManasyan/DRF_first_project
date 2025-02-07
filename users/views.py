import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from web_sky.models import Course

from .models import Payment
from .services import (create_checkout_session, create_price, create_product)


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


@csrf_exempt
def create_payment_session(request):
    if request.method == "POST":
        # Если данные приходят в формате JSON
        if request.content_type.startswith('application/json'):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        else:
            data = request.POST

        course_id = data.get("course_id")
        amount_value = data.get("amount")

        # Проверяем наличие необходимых данных
        if course_id is None:
            return JsonResponse({'error': 'Не указан course_id'}, status=400)
        if amount_value is None:
            return JsonResponse({'error': 'Не указана сумма оплаты (amount)'}, status=400)

        try:
            amount = int(amount_value)
        except ValueError:
            return JsonResponse({'error': 'Неверный формат суммы оплаты'}, status=400)

        # Получаем данные о курсе, предполагаем, что такая модель существует
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Курс не найден'}, status=404)

        # Шаг 1: Создаем продукт в Stripe
        product_id = create_product(course.name)
        if isinstance(product_id, dict) and product_id.get('error'):
            return JsonResponse({'error': product_id['error']}, status=400)

        # Шаг 2: Создаем цену в Stripe (обратите внимание, что сумма в копейках)
        price_id = create_price(product_id, amount)
        if isinstance(price_id, dict) and price_id.get('error'):
            return JsonResponse({'error': price_id['error']}, status=400)

        # Определяем URL для успешного завершения и отмены
        success_url = "http://localhost:8000/payments/success/"
        cancel_url = "http://localhost:8000/payments/cancel/"

        # Шаг 3: Создаем сессию оплаты
        session_url = create_checkout_session(price_id, success_url, cancel_url)
        if isinstance(session_url, dict) and session_url.get('error'):
            return JsonResponse({'error': session_url['error']}, status=400)

        # Сохраняем информацию о платеже (при условии, что пользователь аутентифицирован)
        Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            method='transfer'
        )

        return JsonResponse({'checkout_url': session_url})
    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)