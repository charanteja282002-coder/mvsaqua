from django.urls import path
from . import views
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('track/', views.track, name='track'),
    path('invoice/<str:order_id>/', views.invoice_pdf, name='invoice'),
]
