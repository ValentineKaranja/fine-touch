from django.shortcuts import render, redirect
from .models import ProductName, ProductServices, Order, Customer
from .forms import OrderForm

# Create your views here.
def home(request):
    products = ProductName.objects.all()
    return render(request, 'index.html', {'products':products})


def product(request, slug):
    details = ProductServices.objects.filter(product_name__slug=slug)
    return render(request, 'prods.html', {'details':details})


def services(request):
    return render(request, 'services.html')

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


def store(request):
    return render(request, 'store.html')