from django.shortcuts import render, get_object_or_404
from .models import Profile
from checkout.models import CheckoutOrder
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages


@login_required
def profile_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your info were successfully updated')

    orders = profile.profile_orders.all()
    order_count = 0
    for order in orders:
        order_count += 1

    form = ProfileForm(instance=profile)

    template = 'profiles/profile_page.html'
    context = {
        'order_count': order_count,
        'form': form,
        'profile': profile,
        'orders': orders,
    }
    return render(request, template, context)


def profile_order_history(request, order_number):
    order = get_object_or_404(CheckoutOrder, order_number=order_number)
    from_profile_page = True
    template = 'checkout/checkout_completed.html'
    context = {
        'order': order,
        'from_profile_page': from_profile_page,
    }
    return render(request, template, context)
