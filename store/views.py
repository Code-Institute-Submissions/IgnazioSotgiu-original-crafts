from django.shortcuts import render, get_object_or_404
from .models import Product


def display_homepage(request):
    """ Display the homepage """
    template = 'store/index.html'
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, template, context)


def products(request):
    """ display all products in e store - all products page """
    products = Product.objects.all()
    template = 'store/products.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def single_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    template = 'store/single_product.html'
    context = {
        'product': product,
    }
    return render(request, template, context)
