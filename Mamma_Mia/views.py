import logging
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.decorators import api_view,  action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.utils import json
from Mamma_Mia.serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


logger = logging.getLogger(__name__)


@api_view(["POST"])
def create_customer(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')

    # Проверяем, что имя пользователя и пароль переданы
    if not username or not password:
        response_data = {"error": "Имя пользователя и пароль обязательны."}
        logger.error("Имя пользователя и пароль обязательны.")
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Создаем пользователя Django
        user = User.objects.create_user(username=username, password=password)
        response_data = {
            "message": "Пользователь успешно зарегистрирован.",
            "user": {
                "id": user.id,
                "username": user.username,
            }
        }
        logger.info(f"Пользователь успешно зарегистрирован: {username}")
        return Response(response_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {str(e)}")
        response_data = {"error": "Ошибка при регистрации пользователя."}
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IsAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class AllowAll(permissions.BasePermission):
    """
    Custom permission to allow all users.
    """
    def has_permission(self, request, view):
        return True


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOnly]  # Общее разрешение для всех методов, кроме 'list'

    def perform_action(self, action, instance=None, data=None):
        try:
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            getattr(self, f'perform_{action}')(serializer)
            instance_id = instance.id if instance else serializer.data.get('id')
            logging.info(f'{action.capitalize()}d ingredient {instance_id}: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_201_CREATED) if action == 'create' else Response(serializer.data)
        except Exception as e:
            logging.error(f'Error {action}ing ingredient: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[AllowAll])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminOnly, permissions.IsAuthenticated])
    def create(self, request, *args, **kwargs):
        return self.perform_action('create', data=request.data)

    @action(detail=True, methods=['delete'], permission_classes=[IsAdminOnly, permissions.IsAuthenticated])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            logging.info(f'Deleted ingredient {instance.id}')
            return Response({'message': 'Ingredient deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(f'Error deleting ingredient: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_action(self, action, instance=None, data=None):
        try:
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            getattr(self, f'perform_{action}')(serializer)
            instance_id = instance.id if instance else serializer.data.get('id')
            logging.info(f'{action.capitalize()}d pizza {instance_id}: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_201_CREATED) if action == 'create' else Response(serializer.data)
        except Exception as e:
            logging.error(f'Error {action}ing pizza: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        return self.perform_action('create', data=request.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance_id = instance.id
        logging.info(f'Updated pizza {instance_id}: {serializer.data}')
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            logging.info(f'Deleted pizza {instance.id}')
            return Response({'message': 'Pizza deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(f'Error deleting pizza: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    permission_classes = [AllowAll]

    def perform_action(self, action, instance=None, data=None, partial=False):
        try:
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            getattr(self, f'perform_{action}')(serializer)
            instance_id = instance.id if instance else serializer.data.get('id')
            logging.info(f'{action.capitalize()}d topping {instance_id}: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_201_CREATED) if action == 'create' else Response(serializer.data)
        except Exception as e:
            logging.error(f'Error {action}ing topping: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        return self.perform_action('create', data=request.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.perform_action('update', instance=instance, data=request.data, partial=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            logging.info(f'Deleted topping {instance.id}')
            return Response({'message': 'Topping deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(f'Error deleting topping: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_action(self, action, instance=None, data=None):
        try:
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            getattr(self, f'perform_{action}')(serializer)
            instance_id = instance.id if instance else serializer.data.get('id')
            logging.info(f'{action.capitalize()}d order {instance_id}: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_201_CREATED) if action == 'create' else Response(serializer.data)
        except Exception as e:
            logging.error(f'Error {action}ing order: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        return self.perform_action('create', data=request.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            logging.info(f'Hard deleted order {instance.id}')
            return Response({'message': 'Order hard deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(f'Error hard deleting order: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]


def ping(request):
    logger.info(f"run server")
    return HttpResponse("<h1 style=color:blue> Hello, world. You're at the </h1>")
