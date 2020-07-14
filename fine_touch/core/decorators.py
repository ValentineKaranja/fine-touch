from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):  # takes in a view function i.e register or login view
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  # checks if user is authenticated and redirects to home page
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)  # if not user is allowed to login or register

    return wrapper_func