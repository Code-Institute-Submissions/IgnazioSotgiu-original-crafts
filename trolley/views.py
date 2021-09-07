from django.shortcuts import render, redirect


def view_trolley(request):
    """ A view to display the trolley"""

    return render(request, 'trolley/view_trolley.html')


def add_to_trolley(request, product_id):

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    trolley = request.session.get('trolley', {})

    if product_id in list(trolley.keys()):
        trolley[product_id] += quantity
    else:
        trolley[product_id] = quantity

    request.session['trolley'] = trolley
    return redirect(redirect_url)
