from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.food_menu, name='food_menu'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    path('add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]