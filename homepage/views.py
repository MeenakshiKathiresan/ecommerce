from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse


# Create your views here.
def home_view(request):
    products = Product.objects.filter(trending=True)
    cart_count = get_cart_qty(request)
    context = {'products': products, 'cart_count':cart_count}
    return render(request, 'home.html', context)


def store_view(request):
    cart_count = get_cart_qty(request)
    if 'term' in request.GET:
        products = Product.objects.filter(name__contains = request.GET.get('term'))
        names = [product.name for product in products]
        print(names, " titles")
        return JsonResponse(names, safe=False)

    search_word = ""
    if request.method == "POST":
        search_word = request.POST['search_word']
        products = Product.objects.filter(name__contains=search_word)

    else:
        products = Product.objects.all()

    context = {'products': products, 'searched_word': search_word, 'cart_count':cart_count}
    return render(request, 'store.html', context)


def cart_view(request):
    if request.user.is_authenticated:

        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, status=False)

        if request.method == "POST":
            prod_id = request.POST['item']
            OrderItem.objects.filter(order=order, product=prod_id).delete()

        # get all items in this order
        items = order.orderitem_set.all()

    else:
        items = {}
        print("need to authenticate")
        return render(request, 'login.html', {})

    cart_count = get_cart_qty(request)

    context = {'items': items, 'order': order, 'cart_count': cart_count}
    return render(request, 'cart.html', context)


def order_complete_view(request):
    if request.body:
        data = json.loads(request.body)
        order = data['order']
        # save shipping address with order, customer
        Order.objects.filter(id=order).update(status=True)

    orders = Order.objects.filter(customer=request.user, status=True)
    orders_dict = {}

    for order in orders:
        orders_dict[order] = order.orderitem_set.all()

    cart_count = get_cart_qty(request)
    context = {'orders': orders_dict, 'cart_count': cart_count}
    return render(request, 'order_history.html', context)



def checkout_view(request):

    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(customer=customer, status=False)
        order = order[0]

        # get all items in this order
        items = order.orderitem_set.all()
    else:
        items = {}
        print("need to authenticate")
        return render(request, 'login.html', {})

    cart_count = get_cart_qty(request)
    context = {'items': items, 'order': order, 'cart_count': cart_count}
    return render(request, 'checkout.html', context)


def about_view(request):
    cart_count = get_cart_qty(request)
    context = {'cart_count': cart_count}
    return render(request, 'about.html', context)

def login_view(request):
    cart_count = get_cart_qty(request)
    context = {'cart_count': cart_count}
    return render(request, 'login.html', context)

@login_required()
def product_details_view(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        user = request.user

        count = 0
        # if request to update quantity, get order or create order and update quantity
        # else check if item in ordered items and get quantity
        if request.method == "POST":
            data = json.loads(request.body)
            prod_quantity = int(data['qty'])

            order, created = Order.objects.get_or_create(customer=user, status=False)

            if OrderItem.objects.filter(product=product, order=order).exists():
                order_item = OrderItem.objects.filter(product=product, order=order)[0]
                prod_quantity += order_item.quantity
                count = prod_quantity
                OrderItem.objects.filter(product=product, order=order).update(quantity=prod_quantity)
            else:
                order_item = OrderItem.objects.create(product=product, order=order, quantity=prod_quantity)
                order_item.save()

        order = Order.objects.filter(customer=request.user, status=False)

        if order:
            order = order[0]

            if OrderItem.objects.filter(product=product, order=order).exists():
                order_item = OrderItem.objects.filter(product=product, order=order)[0]
                count = order_item.quantity

        cart_count = get_cart_qty(request)
        context = {'product': product, 'count': count, 'cart_count': cart_count}

        return render(request, 'product_details.html', context)
    else:
        print("need to authenticate")
        return render(request, 'login.html', {})


def get_cart_qty(request):
    if request.user.is_authenticated:

        orders = Order.objects.filter(customer=request.user, status=False)
        if len(orders) > 0:
            return orders[0].get_item_count

    return 0
