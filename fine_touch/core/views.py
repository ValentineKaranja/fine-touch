from django.shortcuts import render
from .models import ProductName, ProductServices, Order
from .forms import OrderForm

# Create your views here.
def home(request):
    products = ProductName.objects.all()
    return render(request, 'index.html', {'products':products})


def product(request, name):
    details = ProductServices.objects.filter(product_name__name__contains=name)
    return render(request, 'prods.html', {'details':details})


def services(request):
    return render(request, 'services.html')

def order(request, slug):
    customer = request.user
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = Order(
                customer=customer,
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
                product=slug,
            )
            obj.save()
    
    return render(request, 'order.html', {'form': form})


def store(request):
    return render(request, 'store.html')