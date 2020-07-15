from django.http import HttpResponse
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import ProductName, ProductServices, Order, Customer
from .forms import OrderForm, CreateUserForm, CustomerForm


# Create your views here.

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
    return render(request, 'index.html', {'products': products})


def product(request, slug):
    details = ProductServices.objects.filter(product_name__slug=slug)
    return render(request, 'prods.html', {'details': details})


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
def order(request, slug):
    customer = Customer.objects.get(user=request.user)
    product = ProductServices.objects.get(slug=slug)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = Order(
                customer=customer,
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
                product=product,
            )
            obj.save()
            print('item added')
            return redirect('/')

    return render(request, 'order.html', {'form': form})


def about(request):
    return render(request, 'about.html')
