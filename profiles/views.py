from django.shortcuts import render, get_object_or_404
from .models import Profile
from checkout.models import CheckoutOrder
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


@login_required
def profile_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    print(profile)
    orders = profile.profile_orders.all()
    form = ProfileForm(instance=profile)
    print(orders)
    template = 'profiles/profile_page.html'
    context = {
        'form': form,
        'profile': profile,
        'orders': orders,
    }
    return render(request, template, context)
