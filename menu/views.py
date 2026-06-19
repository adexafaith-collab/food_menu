from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import Food


# HOME PAGE
def home(request):
    return render(request, 'menu/home.html')


# FOOD MENU PAGE
def food_menu(request):
    foods = Food.objects.all()
    return render(request, 'menu/food_menu.html', {'foods': foods})


# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.create_user(username=username, password=password)
            return redirect('login')

        except IntegrityError:
            return render(request, 'menu/register.html', {
                'error': 'Username already exists. Try another one.'
            })

    return render(request, 'menu/register.html')


# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('food_menu')
        else:
            return render(request, 'menu/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'menu/login.html')


# ADD TO CART (REAL WORKING VERSION)
def add_to_cart(request, food_id):
    food = Food.objects.get(id=food_id)

    cart = request.session.get('cart', {})
    food_id_str = str(food_id)

    if food_id_str in cart:
        cart[food_id_str] += 1
    else:
        cart[food_id_str] = 1

    request.session['cart'] = cart

    return redirect('view_cart')


# VIEW CART (WITH TOTALS)
def view_cart(request):
    cart = request.session.get('cart', {})

    items = []
    total = 0

    for food_id, qty in cart.items():
        food = Food.objects.get(id=food_id)

        subtotal = food.price * qty
        total += subtotal

        items.append({
            'food': food,
            'qty': qty,
            'subtotal': subtotal
        })

    delivery_fee = 100
    grand_total = total + delivery_fee

    return render(request, 'menu/cart.html', {
        'items': items,
        'total': total,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total
    })