from django.shortcuts import render
from products.models import Product


def home(request):
    """
    Home page: shows all products.
    """
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})
