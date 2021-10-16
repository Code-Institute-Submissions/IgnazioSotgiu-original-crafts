from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from checkout.models import CheckoutOrder
from .forms import ProfileForm
from django.contrib import messages
from reviews.models import Review


def profile_page(request):
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(Profile, user=user)
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(
                    request, 'Your info were successfully updated')

        orders = profile.profile_orders.all().order_by('-order_date')
        order_count = 0
        all_review_product_ids = []
        for order in orders:
            order_count += 1
        reviews = Review.objects.all().filter(author=request.user)
        for review in reviews:
            all_review_product_ids.append(review.product.id)
        form = ProfileForm(instance=profile)

        template = 'profiles/profile_page.html'
        context = {
            'order_count': order_count,
            'form': form,
            'profile': profile,
            'orders': orders,
            'reviews': reviews,
            'all_review_product_ids': all_review_product_ids,
        }
        return render(request, template, context)
    else:
        messages.warning(
            request, 'You need to be logged in to access your profile page')
        return redirect('home')


def profile_order_history(request, order_number):
    if request.user.is_authenticated:
        order = get_object_or_404(CheckoutOrder, order_number=order_number)
        from_profile_page = True
        template = 'checkout/checkout_completed.html'
        context = {
            'order': order,
            'from_profile_page': from_profile_page,
        }
        return render(request, template, context)
    else:
        messages.warning(
            request, 'You need to be logged in to access this information')
        return redirect('home')
