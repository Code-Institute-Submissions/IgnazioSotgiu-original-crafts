from django.shortcuts import render, get_object_or_404
from .models import Product


def display_homepage(request):
    """ Display the homepage """
    template = 'store/index.html'
    return render(request, template)


def products(request):
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
