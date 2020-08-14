from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users
from .models import ProductName, ProductServices, Order, Customer
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductNameForm, ProductServicesForm


# Create your views here.


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_subject.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Mamis Touch',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'Mamis Touch Support <djangologinsmtp@gmail.com>', [user.email],
                                  fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset_form.html",
                  context={"form": password_reset_form})


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context_dict = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context_dict)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Fine-Touch account is disabled.")
        else:
            messages.info(request, 'Username or Password is incorrect')

    context_dict = {

    }
    return render(request, 'accounts/login.html', context=context_dict)


def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    products = ProductName.objects.all()
    paginator = Paginator(products, 5)  # Show 5 services per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})


def product(request, slug):
    details = ProductServices.objects.filter(product_name__slug=slug)
    paginator = Paginator(details, 5)  # Show 5 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'prods.html', {'page_obj': page_obj})


def services(request):
    return render(request, 'services.html')


@login_required(login_url='login')  # decorator redirects one to the login page
# if they try to access this page
def profile(request):
    customer = request.user.customer  # gets current logged in customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            # return redirect('account')
    context_dict = {
        'form': form,
    }
    return render(request, 'customer_profile.html', context=context_dict)


@login_required(login_url='login')  # decorator redirects one to the login page
# if they try to access this page
@allowed_users(allowed_roles=['customer'])
def order(request, slug):
    customer = Customer.objects.get(user=request.user)
    prod = ProductServices.objects.get(slug=slug)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = Order(
                customer=customer,
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
                product=prod,
            )
            obj.save()
            print('item added')
            template = render_to_string('order_mail.html', {'name': customer.name})
            try:
                email = EmailMessage('Your Have Successfully Made an Order', template,
                                     settings.EMAIL_HOST_USER, [customer.email])
                email.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/')

    return render(request, 'order.html', {'form': form})


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['customer'])
def order_list(request):
    orders = Order.objects.filter(customer__user=request.user)
    return render(request, 'order_status.html', {'orders': orders})


def save_order_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            orders = Order.objects.filter(customer__user=request.user)
            data['html_order_list'] = render_to_string('partial_order_list.html', {
                'orders': orders,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['customer'])
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
    else:
        form = OrderForm(instance=order)
    return save_order_form(request, form, 'partial_order_update.html')


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['customer'])
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    data = dict()
    if request.method == 'POST':
        order.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        orders = Order.objects.filter(customer__user=request.user)
        data['html_order_list'] = render_to_string('partial_order_list.html', {
            'orders': orders,
        })
    else:
        context = {'order': order}
        data['html_form'] = render_to_string('partial_order_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['seller'])
def admin_dash(request):
    products = ProductName.objects.all()
    service = ProductServices.objects.all()
    orders = Order.objects.all()
    context = {'products': products,
               'services': service,
               'orders': orders,
               }
    return render(request, 'admin_pages/index.html', context)


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['seller'])
def create_product(request):
    form = ProductNameForm()
    if request.method == 'POST':
        form = ProductNameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dash')

    context_dict = {
        'form': form,
    }
    return render(request, 'admin_pages/add_update.html', context=context_dict)


@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def update_product(request, slug):
    prod = ProductName.objects.get(slug=slug)
    form = ProductNameForm(instance=product)  # prefills the form to be updated
    if request.method == 'POST':
        form = ProductNameForm(request.POST, request.FILES,
                               instance=prod)  # this enables the form to be saved only in this instance
        # not as a new form
        if form.is_valid():
            form.save()
            return redirect('admin_dash')
    context_dict = {
        'form': form,
    }
    return render(request, 'admin_pages/add_update.html', context=context_dict)


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['seller'])  # decorator ensures only an admin can log in into this page
def delete_product(request, slug):
    prod = ProductName.objects.get(slug=slug)
    if request.method == 'POST':
        prod.delete()
        return redirect('admin_dash')
    context_dict = {
        'product': product,
    }
    return render(request, 'admin_pages/delete.html', context=context_dict)


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
@allowed_users(allowed_roles=['seller'])  # decorator ensures only an admin can log in into this page
def create_service(request):
    form = ProductServicesForm()
    if request.method == 'POST':
        form = ProductServicesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dash')

    context_dict = {
        'form': form,
    }
    return render(request, 'admin_pages/add_update.html', context=context_dict)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def update_service(request, slug):
    service = ProductServices.objects.get(slug=slug)
    form = ProductServicesForm(instance=service)  # prefills the form to be updated
    if request.method == 'POST':
        form = ProductServicesForm(request.POST, request.FILES,
                                   instance=service)  # this enables the form to be saved only in this instance
        # not as a new form
        if form.is_valid():
            form.save()
            return redirect('admin_dash')
    context_dict = {
        'form': form,
    }
    return render(request, 'admin_pages/add_update.html', context=context_dict)


@login_required(login_url='login')  # decorator redirects one to the login page if they try to access this page
# @allowed_users(allowed_roles=['admin'])  # decorator ensures only an admin can log in into this page
def delete_service(request, slug):
    service = ProductServices.objects.get(slug=slug)
    if request.method == 'POST':
        service.delete()
        return redirect('admin_dash')
    context_dict = {
        'service': service,
    }
    return render(request, 'admin_pages/delete.html', context=context_dict)
