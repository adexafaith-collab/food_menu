from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Cart, CartItem


# 1. HOME PAGE
def home(request):
    foods = Food.objects.all()
    return render(request, 'home.html', {'foods': foods})


# 2. ADD TO CART
def add_to_cart(request, food_id):
    cart, _ = Cart.objects.get_or_create(id=1)

    food = get_object_or_404(Food, id=food_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food
    )

    if created:
        item.quantity = 1
    else:
        item.quantity += 1

    item.save()

    return redirect('home')


# 3. VIEW CART  👈 THIS IS WHERE YOUR CODE GOES
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(id=1)
    items = CartItem.objects.filter(cart=cart)

    subtotal = 0

    for item in items:
        subtotal += item.quantity * 100

    delivery_fee = 150

    total = subtotal + delivery_fee

    return render(request, 'cart.html', {
        'items': items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total
    })