from django.urls import path
from . import views
urlpatterns = [
    path('', views.dash_home, name='dash_home'),
    path('login/', views.dash_login, name='dash_login'),
    path('logout/', views.dash_logout, name='dash_logout'),
    path('products/', views.dash_products, name='dash_products'),
    path('products/add/', views.product_form, name='dash_product_add'),
    path('products/edit/<int:pk>/', views.product_form, name='dash_product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='dash_product_delete'),
    path('orders/', views.dash_orders, name='dash_orders'),
    path('orders/<int:pk>/', views.dash_order, name='dash_order'),
    path('categories/', views.dash_categories, name='dash_categories'),
    path('reviews/', views.dash_reviews, name='dash_reviews'),
]
