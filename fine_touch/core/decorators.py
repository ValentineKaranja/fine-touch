from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):  # takes in a view function i.e register or login view
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  # checks if user is authenticated and redirects to home page
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)  # if not user is allowed to login or register

    return wrapper_func


# def allowed_users(allowed_roles=[]):  # a single page can allow multiple types of users passed into the list
#     def decorator(view_func):  # takes in the view function
#         def wrapper_func(request, *args, **kwargs):  # checks the allowed roles and enforces them

#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse('You are not authorised to view this page')
#         return wrapper_func
#     return decorator


# def admin_only(view_func):  # restricts users from viewing the home view smartly
#     # takes in a view function
#     def wrapper_func(request, *args, **kwargs):  # this is a quick fix not suitable for production
#         group = None

#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name

#         if group == 'customer':
#             return redirect('user_page')

#         if group == 'admin':
#             return view_func(request, *args, **kwargs)

#     return wrapper_func