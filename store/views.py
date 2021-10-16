from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponseRedirect)
from django.contrib import messages
from django.db.models import Q
from reviews.models import Review
from .models import Product, Category
from .forms import ProductForm


def display_homepage(request):
    """ Display the homepage """
    template = 'store/index.html'
    products = Product.objects.all().filter(add_to_popular_products=True)
    context = {
        'products': products,
    }
    return render(request, template, context)


def products(request):
    """ display all products in e store - all products page """
    products = Product.objects.order_by('-updated', '-created')
    template = 'store/products.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def best_sellers(request):
    """ display Best sellers - Fast selling products """
    products = Product.objects.filter(
        selling_fast_tag=True).order_by('-updated', '-created')
    template = 'store/best_sellers.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def original_gallery(request):
    """ display Best sellers - Fast selling products """
    products = Product.objects.filter(
        original_tag=True).order_by('-updated', '-created')
    template = 'store/original_gallery.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def accessories(request):
    """ display Accessories - Accessories page """
    accessories = Category.objects.get(name='accessories')
    products = Product.objects.filter(
        category=accessories).order_by('-updated', '-created')
    template = 'store/accessories.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def paint_by_numbers(request):
    """ display Paint by Numbers - Paint by Numbers page """
    paint_by_numbers = Category.objects.get(name='paint_by_numbers')
    products = Product.objects.filter(
        category=paint_by_numbers).order_by('-updated', '-created')
    template = 'store/paint_by_numbers.html'
    context = {
        'products': products,
    }
    return render(request, template, context)


def about_page(request):
    """
    A view to display the about page
    """
    template = 'store/about_page.html'
    return render(request, template)


def contact_page(request):
    """ a view to display the contact page """

    template = 'store/contact_page.html'
    return render(request, template)


def single_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.all().filter(
        product=product_id).order_by('-review_date')
    reviews_count = 0
    for review in reviews:
        reviews_count += 1
    template = 'store/single_product.html'
    context = {
        'product': product,
        'reviews': reviews,
        'reviews_count': reviews_count,
    }
    return render(request, template, context)

# code taken from code institute lecture


def search_result(request):

    """ display search result - search result page """
    products = Product.objects.order_by('-updated', '-created')
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
                messages.warning(request, 'Enter a valid search parameter')
                return redirect(reverse('home'))

            products = products.filter(
                search_terms).order_by('-updated', '-created')

    for product in products:
        if product.number_in_stock > 0 and not product.hide_product:
            total_items += 1

    template = 'store/search_result.html'
    context = {
        'products': products,
        'query': query,
        'total_items': total_items,
        'selected_categories': selected_categories,
    }
    return render(request, template, context)


def hidden_products(request):
    """ display hidden products to the admin """
    if request.user.is_superuser:
        products = Product.objects.filter(hide_product=True)
        template = 'store/hidden_products.html'
        context = {
            'products': products,
        }
        return render(request, template, context)

    else:
        messages.error(request, 'Only Admin can access this link')
        return redirect('home')


def out_of_stock_products(request):
    """ display out of stock products to the admin """
    if request.user.is_superuser:
        out_of_stock_products = []
        products = Product.objects.all()
        for product in products:
            if product.number_in_stock == 0:
                out_of_stock_products.append(product)
        template = 'store/out_of_stock_products.html'
        context = {
            'products': out_of_stock_products,
        }
        return render(request, template, context)
    else:
        messages.error(request, 'Only Admin can access this link')
        return redirect('home')


def add_product(request):
    """
    add product to the database
    """
    if request.user.is_superuser:
        form = ProductForm()

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            next = request.POST.get('next')
            if form.is_valid:
                form.save()
                messages.success(request, 'Product successfully added to store')
                return HttpResponseRedirect(next)

        template = 'store/add_product.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'Only Admin can access this link')
        return redirect('home')


def update_product(request, product_id):
    """
    update product already in the database
    """
    if request.user.is_superuser:
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)

        if request.method == 'POST':
            next = request.POST.get('next')
            try:
                form = ProductForm(
                    request.POST, request.FILES, instance=product)
                if form.is_valid:
                    form.save()
                    messages.success(request, 'Product successfully updated')
                    return redirect('products')
            except ValueError:
                messages.error(request, 'The form submitted \
                    was invalid. Please enter valid data')
                return HttpResponseRedirect(next)

        template = 'store/update_product.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'Only Admin can access this link')
        return redirect('home')


def delete_warning(request, product_id):
    """
    A view make sure the admin is deleting the right product
    Last step before deleting product
    """
    if request.user.is_superuser:
        product = Product.objects.get(id=product_id)

        template = 'store/delete_product_warning.html'
        context = {
            'product': product,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'Only Admin can access this function')
        return redirect('home')


def delete_product(request, product_id):
    """
    Delete product from the database
    """
    if request.user.is_superuser:
        product = Product.objects.get(id=product_id)
        try:
            product.delete()
            messages.success(request, f'{product.name} was successfully deleted')
            return redirect('products')

        except ValueError:
            messages.error(request, f'Request denied! \
                Was not possible to delete {product.name} from the database')
            return redirect('products')
    else:
        messages.error(request, 'Only Admin can access this function')
        return redirect('home')

# handle the error 404 and 500


def error_404(request, exception, template_name="store/404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def error_500(request, *args, **argv):
    return render(request, 'store/500.html', status=500)
