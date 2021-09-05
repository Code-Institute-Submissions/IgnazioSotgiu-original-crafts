from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
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

# code taken from code institute lecture


def search_result(request):

    """ display search result - search result page """
    products = Product.objects.all()

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if query:
                search_terms = Q(name__icontains=query) | Q(
                    description__icontains=query)
            products = products.filter(search_terms)

    template = 'store/search_result.html'
    context = {
        'products': products,
        'search': query
    }
    return render(request, template, context)
