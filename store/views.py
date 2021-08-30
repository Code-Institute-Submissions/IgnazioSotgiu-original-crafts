from django.shortcuts import render
from .models import Product

# Create your views here.


def display_homepage(request):
    template = 'store/index.html'
    return render(request, template)
