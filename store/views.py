from django.shortcuts import render


def display_homepage(request):
    """ Display the homepage """
    template = 'store/index.html'
    return render(request, template)
