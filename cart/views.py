from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from .csv_utils import create_order_csv


def cart_detail(request):
    """
    Show the contents of the cart.
    """
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    """
    Add a product to the cart. Not allowed if the product is out of stock.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    if product.is_out_of_stock():
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect('products:product_detail', pk=product.id)

    cart.add(product=product, quantity=1)
    messages.success(request, f'"{product.name}" was added to your cart.')
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, 'The product was removed from your cart.')
    return redirect('cart:cart_detail')


def cart_update(request, product_id):
    """
    Update the quantity of a product in the cart via a POST form.
    """
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        product = get_object_or_404(Product, id=product_id)

        # Don't allow a quantity greater than the available stock
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} units of "{product.name}" are available.')
            quantity = product.stock

        if quantity <= 0:
            messages.error(request, 'Quantity must be greater than zero.')
        else:
            cart = Cart(request)
            cart.update(product_id, quantity)
            messages.success(request, 'Quantity updated.')

    return redirect('cart:cart_detail')


@login_required
def checkout(request):
    """
    Complete the purchase:
    1. Check that the requested quantity is available for every product.
    2. If available: save the order, reduce stock, generate a CSV file,
       and empty the cart.
    3. If not available: show an error message and don't complete anything.
    """
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, 'Your cart is empty, add some products first.')
        return redirect('cart:cart_detail')

    # Step 1: check that every requested quantity is available before
    # changing anything
    for item in cart:
        product = item['product']
        quantity = item['quantity']
        if quantity > product.stock:
            messages.error(
                request,
                f'Sorry, only {product.stock} units of "{product.name}" are available.'
            )
            return redirect('cart:cart_detail')

    # Step 2: everything is available, save the order and reduce stock.
    # transaction.atomic makes sure all these operations succeed together,
    # or none of them are applied if something goes wrong.
    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_price=0)
        total_price = 0

        for item in cart:
            product = item['product']
            quantity = item['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            # Reduce the stock
            product.stock -= quantity
            product.save()

            total_price += product.price * quantity

        order.total_price = total_price
        order.save()

    # Step 3: generate a CSV file for this purchase
    create_order_csv(order)

    # Empty the cart
    cart.clear()

    messages.success(request, f'Your order has been confirmed! Order #: {order.id}')
    return redirect('cart:order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    """
    Order confirmation page.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_success.html', {'order': order})
