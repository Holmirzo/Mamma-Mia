from urllib import request

from django.urls import path
from Mamma_Mia.views import *

urlpatterns = [
    path('', ping, name='ping'),
    path('ingredients/', IngredientViewSet.as_view({'get': 'list'}), name='ingredients_read'),
    path('ingredients/<int:pk>/', IngredientViewSet.as_view({'get': 'retrieve'}), name='ingredient_read'),
    path('ingredients/new_ingr/', IngredientViewSet.as_view({'post': 'create'}), name='ingredients_create'),
    path('ingredients/<int:pk>/details/', IngredientViewSet.as_view({'delete': 'destroy'}), name='ingredient_delete'),

    path('pizzas/', PizzaViewSet.as_view({'get': 'list'}), name='pizzas_read'),
    path('pizza/<int:pk>/', PizzaViewSet.as_view({'get': 'retrieve'}), name='pizza_read'),
    path('pizzas/new_pizza/', PizzaViewSet.as_view({'post': 'create'}), name='pizza_create'),
    path('pizzas/<int:pk>/details/', PizzaViewSet.as_view({'delete': 'destroy'}), name='pizza_delete'),
    path('pizzas/<int:pk>/update/', PizzaViewSet.as_view({'put': 'update'}), name='pizza_update'),

    path('toppings/', ToppingViewSet.as_view({'get': 'list'}), name='toppings_read'),
    path('toppings/<int:pk>/', ToppingViewSet.as_view({'get': 'retrieve'}, name='topping_read')),
    path('toppings/new_topp/', ToppingViewSet.as_view({'post': 'create'}), name='toppings_create'),
    path('toppings/<int:pk>/details/', ToppingViewSet.as_view({'delete': 'destroy'}), name='toppings_delete'),
    path('toppings/<int:pk>/update/', ToppingViewSet.as_view({'patch': 'update'}), name='toppings_update'),

    path('orders/', OrderViewSet.as_view({'get': 'list'}), name='orders_read'),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve'}, name='order_read')),
    path('orders/new_order/', OrderViewSet.as_view({'post': 'create'}), name='orders_create'),

    path('customers/', UserViewSet.as_view({'get': "list"}), name='customers_read'),
    path('customers/<int:pk>/', UserViewSet.as_view({'retrieve': 'retrieve'}), name='customers_read'),
    path('customers/new_customer/', UserViewSet.as_view({'post': 'create'}), name='customers_create'),

    path('ideas/', IdeaViewSet.as_view({'get': 'list'}), name='ideas_read'),
    path('ideas/<int:pk>/', IdeaViewSet.as_view({'get': 'retrieve'}), name='ideas_read'),
    path('ideas/new_idea/', IdeaViewSet.as_view({'post': 'create'}), name='ideas_create'),
    path('ideas/<int:pk>/update/', IdeaViewSet.as_view({'put': 'update'}), name='ideas_update'),
    path('ideas/<int:pk>/delete/', IdeaViewSet.as_view({'delete': 'destroy'}, name='ideas_delete')),

    path('comments/', CommentViewSet.as_view({'get': 'list'}), name=''),
    path('comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve'}), name=''),
    path('comments/new_comment/', CommentViewSet.as_view({'post': 'create'}), name='comments_create'),
    path('comments/<int:pk>/update/', CommentViewSet.as_view({'put': 'update'}), name='comments_update'),
    path('comments/<int:pk>/delete/', CommentViewSet.as_view({'delete': 'destroy'}), name='comments_delete'),

    path('complaints/', ComplaintViewSet.as_view({'get': 'list'}), name='complaints_list'),
    path('complaints/<int:pk>/', ComplaintViewSet.as_view({'get': 'retrieve'}), name='complaints_retrieve'),
    path('complaints/new_complaint/', ComplaintViewSet.as_view({'post': 'create'}), name='complaints_update'),
    path('complaints/<int:pk>/update/', ComplaintViewSet.as_view({'put': 'update'}), name='complaints_update'),
    path('complaints/<int:pk>/delete/', ComplaintViewSet.as_view({'delete': 'destroy'}), name='complaints_delete')
]
