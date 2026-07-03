from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),
    path('menu/', views.food_menu, name='food_menu'),
    path('contact/', views.contact, name='contact'),

    # AUTHENTICATION
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # FOOD MANAGEMENT
    path('add-food/', views.add_food, name='add_food'),
    path('delete-food/<int:food_id>/', views.delete_food, name='delete_food'),

    # CART
    path('add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ADMIN
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-order/<int:order_id>/', views.update_order_status, name='update_order'),
]