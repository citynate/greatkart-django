from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart=request.session.create() # create new cart if no cart
    return cart

def add_cart(request, product_id):
    product=Product.objects.get(id=product_id) # get the product
    product_variation=[]
    if request.method == 'POST':
        #color= request.POST['color']
        #size=request.POST['size']
        for item in request.POST:
            key=item
            value = request.POST[key]
            #print(key, value)

            try:
                variation=Variation.objects.get(product=product, variation_category__iexact=key,variation_values__iexact=value)
                #print(variation)
                #print('this is variation')
                product_variation.append(variation)
                #print(product_variation)
                #print('this is product_variation')
            except:
                #print ('try failed')
                pass
    try: 
        cart=Cart.objects.get(cart_id=_cart_id(request)) # get the cart from the session id
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    print(is_cart_item_exists)
    if is_cart_item_exists:
    
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        #existing variations -> database
        #current variation -> product variation
        #item id -> database
        ex_var_list = []
        id=[]
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            #increase cart items
            index = ex_var_list.index(product_variation)
            item_id=id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity+=1
            item.save()

            #return HttpResponse('True')
        else:
            #create new cart items
            #return HttpResponse('False')
            item=CartItem.objects.create(product=product, quantity=1, cart=cart)

            if len(product_variation)>0:
                item.variation.clear()
                item.variation.add(*product_variation)

        #cart_item.quantity +=1
            item.save()
    else :
        cart_item=CartItem.objects.create(
            product = product,
            cart=cart,
            quantity = 1,
        ) 
        if len(product_variation)>0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()
    #return HttpResponse(cart_item.product)
    return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax=(9*total)/100
        grand_total = total + tax

    except cart.ObjectNotExist:
        pass

    context = {
        'total':total, 
        'quantity':quantity,
        'cart_items':cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context=context)