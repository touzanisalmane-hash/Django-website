from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):
    """
    Show all products (also used for the home page).
    """
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    """
    Show the details of a single product, looked up by its id (pk).
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
