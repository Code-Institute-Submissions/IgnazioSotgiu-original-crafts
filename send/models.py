from django.db import models

# Create your models here.


class Contact(models.Model):
    from_email = models.EmailField(max_length=254, null=False, blank=False)
    recipient_list = models.EmailField(max_length=254, null=False, blank=False)
    email_subject = models.CharField(max_length=254, null=False, blank=False)
    message = models.TextField(max_length=1024, null=False, blank=False)
    email_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email_subject
