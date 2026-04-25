

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from .models import Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def home(request):
    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    cart_items = []
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'home.html', {
        'products': products,
        'cart_items': cart_items
    })



@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')





@login_required(login_url='/login/')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum([item.total_price() for item in items])

    if request.method == "POST":
     address = request.POST.get('address')
    phone = request.POST.get('phone')

    if not phone:
        return render(request, 'checkout.html', {
            'items': items,
            'total': total,
            'error': 'Phone number is required!'
        })

    order = Order.objects.create(
        user=request.user,
        phone=phone,
        address=address,
        total_price=total
    )
    for item in items:
            OrderItem.objects.create(
             order=order,
                product=item.product,
                quantity=item.quantity
            )

            items.delete()

    return render(request, 'success.html')

    return render(request, 'checkout.html', {'items': items, 'total': total})





def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'items': items})


def logout_view(request):
    logout(request)
    return redirect('home')  