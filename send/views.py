from django.shortcuts import (
    render, redirect, reverse)
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm


def send_email(request):
    contact_form = ContactForm()
    recipient_list = []

    if request.method == 'POST':
        from_email = request.POST['from_email']
        recipient_list = settings.DEFAULT_FROM_EMAIL
        email_subject = request.POST['email_subject']
        message = request.POST['message']

        form_data = {
            'from_email': from_email,
            'recipient_list': recipient_list,
            'email_subject': email_subject,
            'message': message,
        }

        contact_form = ContactForm(form_data)
        if contact_form.is_valid():
            contact_form.save()

            send_mail(email_subject, message, from_email, [recipient_list],
                      fail_silently=False)

            messages.success(request, 'Thank You to get in touch, \
                your email was successfully sent')
            return redirect('contact_page')

        else:
            messages.error(
                request, 'The form is not valid, Please enter a valid form')
            return redirect(reverse('send_email'))

    contact_form = ContactForm()
    template = 'send/send_email.html'
    context = {
        'contact_form': contact_form,
    }
    return render(request, template, context)
