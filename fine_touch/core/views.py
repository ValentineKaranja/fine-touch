from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')


def product(request):
    return render(request, 'prods.html')


def services(request):
    return render(request, 'services.html')

def order(request):
    return render(request, 'order.html')


def store(request):
    return render(request, 'store.html')