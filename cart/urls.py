from django.urls import path
from . import views
urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add/<int:pk>/', views.cart_add, name='cart_add'),
    path('update/<int:pk>/', views.cart_update, name='cart_update'),
    path('remove/<int:pk>/', views.cart_remove, name='cart_remove'),
]
