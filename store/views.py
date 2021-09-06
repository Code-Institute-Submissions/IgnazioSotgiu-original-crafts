from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


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
    categories = None
    query = None
    total_items = 0
    selected_categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            category = Category.objects.filter(name__in=categories)
            selected_categories = category

        if 'q' in request.GET:
            query = request.GET['q']
            if query:
                search_terms = Q(name__icontains=query) | Q(
                    description__icontains=query)

            else:
                messages.error(request, 'Enter a valid search parameter')
                return redirect(reverse('home'))

            products = products.filter(search_terms)

    total_items = len(products)
    template = 'store/search_result.html'
    context = {
        'products': products,
        'query': query,
        'total_items': total_items,
        'selected_categories': selected_categories,
    }
    return render(request, template, context)
