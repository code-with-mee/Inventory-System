from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/submit/', views.order_submit, name='order_submit'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/report/', views.order_report, name='order_report'),
]
