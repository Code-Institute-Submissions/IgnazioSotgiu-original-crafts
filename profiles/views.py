from django.shortcuts import render


def profile_page(request):
    return render(request, 'profiles/profile_page.html')
