from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    # ✅ FIX: REQUIRED FOR CART CALCULATIONS
    price = models.IntegerField(default=100)

    image = models.ImageField(upload_to='foods/', blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_total(self):
        return self.food.price * self.quantity