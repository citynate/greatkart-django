from django.shortcuts import render
from store.models import Product

def home(response):
    products=Product.objects.all().filter(is_available=True)
    #add a contect variable appears to allow us to pass any variables to html

    context = {
        'products':products,
    }

    return render(response, 'home.html', context=context)