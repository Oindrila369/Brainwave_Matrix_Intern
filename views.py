from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Wishlist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  # ✅ Import login here
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})



# Cart view
def cart(request):
    # Fetch cart items for the user
    cart_items = request.user.cart.all()  # Assuming you have a Cart model related to the User
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

# My Orders view
def my_orders(request):
    orders = Order.objects.filter(user=request.user)  # Assuming Order model
    return render(request, 'store/my_orders.html', {'orders': orders})

# Buy Now functionality
def buy_now(request, product_id):
    product = Product.objects.get(id=product_id)
    order = Order.objects.create(user=request.user, product=product)
    messages.success(request, "Order placed successfully!")
    return redirect('my_orders')  # Redirect to orders page

# Cancel Order functionality
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()  # Or set a status like "Cancelled"
    messages.success(request, "Order cancelled successfully!")
    return redirect('my_orders')

def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

def buy_cart_items(request):
    cart = request.session.get('cart', {})
    if cart:
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            Order.objects.create(user=request.user, product=product, quantity=quantity)
        # Clear the cart after the purchase
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('my_orders')  # Redirect to the orders page
    else:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')  # Redirect back to the cart
    
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Check if the product is already in the user's wishlist
    if not Wishlist.objects.filter(user=request.user, product=product).exists():
        Wishlist.objects.create(user=request.user, product=product)
    return redirect('wishlist')  # Redirect to the wishlist page