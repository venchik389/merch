from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})
def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total = product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'total_price': total,
        })
        total_price += total

    return render(request, 'shop/cart_detail.html', {'cart_products': products, 'total_price': total_price})

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')
