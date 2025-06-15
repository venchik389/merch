from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from datetime import datetime

def my_view(request):
    return render(request, 'home.html', {'year': datetime.now().year})

def product_list(request):
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })
def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    # Итерируемся по копии cart (списку ключей), чтобы избежать ошибки
    for product_id in list(cart.keys()):
        quantity = cart[product_id]
        try:
            product = Product.objects.get(pk=product_id)
            total = product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'total_price': total,
            })
            total_price += total
        except Product.DoesNotExist:
            # Безопасно удаляем отсутствующий товар
            del cart[product_id]

    # Обновляем корзину в сессии, если что-то удалили
    request.session['cart'] = cart

    return render(request, 'shop/cart_detail.html', {
        'cart_products': products,
        'total_price': total_price
    })

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
