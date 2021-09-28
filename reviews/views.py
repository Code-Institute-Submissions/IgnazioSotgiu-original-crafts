from django.shortcuts import (
    render, HttpResponseRedirect, get_object_or_404, reverse, redirect)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import Review
from .forms import ReviewForm

# Create your views here.


@login_required
def add_review(request, product_id):
    review_form = ReviewForm()
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        form_data = {
            'product': product,
            'review_title': request.POST['review_title'],
            'review_text': request.POST['review_text'],
            'author': request.user
        }
        review_form = ReviewForm(form_data)
        next = request.POST.get('next')
        if review_form.is_valid:
            user = request.user
            review_form.save()
            messages.success(request, f'Review successfully \
                created. Thank You { user }')
            return HttpResponseRedirect(next)

    template = 'reviews/add_review.html'
    context = {
        'review_form': review_form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review_form = ReviewForm(instance=review)

    if request.method == 'POST':
        next = request.POST.get('next')
        try:
            form_data = {
                'product': review.product,
                'review_title': request.POST['review_title'],
                'review_text': request.POST['review_text'],
                'author': review.author,
            }
            review_form = ReviewForm(form_data, instance=review)
            if review_form.is_valid:
                review_form.save()
                messages.success(request, 'Review successfully updated')
                return redirect(reverse('profile_page'))
        except ValueError:
            messages.error(request, 'The form submitted \
                was invalid. Please enter valid data')
            return HttpResponseRedirect(next)

    template = 'reviews/edit_review.html'
    context = {
        'review_form': review_form,
    }

    return render(request, template, context)

