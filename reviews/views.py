from django.shortcuts import (
    render, HttpResponseRedirect, reverse, redirect)
from django.contrib import messages
from store.models import Product
from .models import Review
from .forms import ReviewForm

# Create your views here.


def add_review(request, product_id):

    if request.user.is_authenticated:
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
            if review_form.is_valid:
                user = request.user
                review_form.save()
                messages.success(request, f'Review successfully \
                    created. Thank You { user }')
                return redirect(reverse('profile_page'))

        template = 'reviews/add_review.html'
        context = {
            'review_form': review_form,
            'product': product,
        }

        return render(request, template, context)
    else:
        messages.error(request, 'Only registered users can access this link')
        return redirect('home')


def edit_review(request, review_id):
    if request.user.is_authenticated:
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
    else:
        messages.error(request, 'Only registered users can access this link')
        return redirect('home')


def delete_review_warning(request, review_id):
    if request.user.is_authenticated:
        review = Review.objects.get(id=review_id)
        if request.user == review.author:

            template = 'reviews/delete_review_warning.html'
            context = {
                'review': review,
            }

            return render(request, template, context)
        else:
            messages.error(request, 'Only author can delete this review ')
            return redirect('profile_page')
    else:
        messages.error(request, 'Only registered users can access this link')
        return redirect('home')


def delete_review(request, review_id):
    if request.user.is_authenticated:
        review = Review.objects.get(id=review_id)
        if request.user == review.author:
            try:
                review.delete()
                messages.success(
                    request, 'The review was successfully deleted')
                return redirect('profile_page')

            except ValueError:
                messages.error(request, 'Request denied! \
                    Was not possible to delete this review from the database')
                return redirect('profile_page')
        else:
            messages.error(request, 'Only author can delete this review ')
            return redirect('profile_page')
    else:
        messages.error(request, 'Only registered users can access this link')
        return redirect('home')
