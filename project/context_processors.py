# -*- coding: utf-8 -*-


from django.contrib.auth.models import User

def customers(request):
    return {
        'customers': User.objects.all(),
    }
