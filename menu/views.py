from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Food, Cart, CartItem, Order


# =========================
# HOME
# =========================
def home(request):
    return render(request, 'menu/home.html')


# =========================
# CONTACT
# =========================
def contact(request):
    return render(request, 'menu/contact.html')


# =========================
# MENU (USER SIDE)
# =========================
def food_menu(request):
    foods = Food.objects.all()
    return render(request, 'menu/food_menu.html', {'foods': foods})


# =========================
# =========================
# REGISTER
# =========================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check if passwords match
        if password1 != password2:
            return render(request, "menu/register.html", {
                "error": "Passwords do not match."
            })

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "menu/register.html", {
                "error": "Username already exists."
            })

        # Create user
        User.objects.create_user(
            username=username,
            password=password1
        )

        return redirect("login")

    return render(request, "menu/register.html")
    


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')

            return redirect('food_menu')

        return render(request, 'menu/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'menu/login.html')

# =========================
# LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    # ADD FOOD
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        if name and price:
            Food.objects.create(
                name=name,
                description=description,
                price=price,
                image=image
            )

        return redirect('admin_dashboard')

    foods = Food.objects.all()
    orders = Order.objects.all().order_by('-created_at')
    users = User.objects.all()

    return render(request, 'menu/admin_dashboard.html', {
        'foods': foods,
        'orders': orders,
        'users': users
    })


# =========================
# ADD FOOD (OPTIONAL PAGE)
# =========================
@login_required
def add_food(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        Food.objects.create(
            name=name,
            description=description,
            price=price,
            image=image
        )

        return redirect('admin_dashboard')

    return render(request, "menu/add_food.html")


# =========================
# ADD TO CART
# =========================
@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('view_cart')




# =========================
# VIEW CART
# =========================
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.cartitem_set.all()

    total = sum(item.item_total() for item in items)
    delivery_fee = 100
    grand_total = total + delivery_fee

    return render(request, 'menu/cart.html', {
        'items': items,
        'total': total,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total
    })


# =========================
# REMOVE FROM CART
# =========================
@login_required
def remove_from_cart(request, food_id):
    cart = Cart.objects.get(user=request.user)
    item = CartItem.objects.get(cart=cart, food_id=food_id)
    item.delete()
    return redirect('view_cart')

# =========================
# PLACE ORDER
# =========================
@login_required
def place_order(request):
    if request.method == "POST":

        cart = Cart.objects.get(user=request.user)
        items = cart.cartitem_set.all()

        if not items:
            return redirect('view_cart')

        items_text = ""
        total_price = 0

        for item in items:
            subtotal = item.item_total()
            items_text += f"{item.food.name} x {item.quantity} = KSh {subtotal}\n"
            total_price += subtotal

        # Add delivery fee
        total_price += 100

        # Save order
        Order.objects.create(
            user=request.user,
            items_text=items_text,
            total_price=total_price
        )

        # Clear cart
        items.delete()

        return redirect('food_menu')

# =========================
# ORDER STATUS UPDATE
# =========================
@login_required
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()

    return redirect('admin_dashboard')


# =========================
# DELETE FOOD
# =========================
@login_required
def delete_food(request, food_id):
    if not request.user.is_staff:
        return redirect('home')

    food = get_object_or_404(Food, id=food_id)
    food.delete()

    return redirect('admin_dashboard')