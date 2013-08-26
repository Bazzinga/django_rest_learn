# -*- coding: utf-8 -*-

# Create your views here.


# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

import datetime

# app specific files

from models import *
from forms import *

from django.contrib.auth.decorators import login_required


def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    t = get_template('depot/create_product.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

@login_required()
def list_product(request):

    list_items = Product.objects.all()
    paginator = Paginator(list_items, 10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depot/list_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))

def view_product(request, id):
    product_instance = Product.objects.get(id = id)

    t=get_template('depot/view_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_product(request, id):

    product_instance = Product.objects.get(id=id)

    form = ProductForm(request.POST or None, instance = product_instance)

    if form.is_valid():
        form.save()

    t=get_template('depot/edit_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

'''
list_items = Product.objects.all()
    paginator = Paginator(list_items, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depot/list_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))
'''

def store_view(request):
    #for ajax!!!
    cart = request.session.get("cart", None)
    products = Product.objects.filter(avalaibleData__lt=datetime.datetime.now().date()).order_by("-avalaibleData")
    paginator = Paginator(products, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        products = paginator.page(page)
    except:
        products = paginator.page(paginator.num_pages)
    # products = Product.objects.order_by("-avalaibleData")
    t = get_template('depot/store.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))

def view_cart(request):
    cart = request.session.get("cart", None)
    t = get_template('depot/view_cart.html')

    if not cart:
        cart = Cart()
        request.session["cart"] = cart

    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))

def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    cart = request.session.get("cart", None)
    if not cart:
        cart = Cart()
        request.session["cart"] = cart
    cart.add_product(product)
    request.session['cart'] = cart
    return view_cart(request)

def clean_cart(request):
    request.session['cart'] = Cart()
    return view_cart(request)

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from depot.models import LineItem
from depot.serializers import ProductSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

from rest_framework.views import View
from serializers import LineItemSerializer

@csrf_exempt
def RESTforCart(request):
    print 'clea i love you'
    if request.method == 'GET':
        items = request.session['cart'].items
        serializer = LineItemSerializer(items)
        return JSONResponse(serializer.data)

@csrf_exempt
def PostCart(request):
    print 'cleantha i love you'
    print request.POST['product']
    product = Product.objects.get(id=request.POST['product'])
    cart = request.session.get("cart", None)
    if not cart:
        cart = Cart()
        request.session["cart"] = cart
    cart.add_product(product)
    request.session['cart'] = cart
    # return request.session['cart'].items
    items = request.session['cart'].items
    serializer = LineItemSerializer(items)
    return JSONResponse(serializer.data)


from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

# app specific files

from models import *
from forms import *
from django.db import transaction

@transaction.commit_on_success
def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        for item in request.session['cart'].items:
            item.order = order
            item.save()
        clean_cart(request)
        return store_view(request)

    t = get_template('depot/create_order.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))



def list_order(request):
  
    list_items = Order.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depot/list_order.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_order(request, id):
    order_instance = Order.objects.get(id = id)

    t=get_template('depot/view_order.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_order(request, id):

    order_instance = Order.objects.get(id=id)

    form = OrderForm(request.POST or None, instance = order_instance)

    if form.is_valid():
        form.save()

    t=get_template('depot/edit_order.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def showPOManytoMany(request):
    product = Product.objects.get(id=1)
    print product.order.all()

    return HttpResponse('manytomany')

def atom_of_order(request, id):
    product = Product.objects.get(id=id)
    for order in product.order.all():
        print order.name

    return HttpResponse('cleantha')
    # t = get_template('depot/atom_order.xml')
    # c=RequestContext(request, locals())
    # return HttpResponse(t.render(c), mimetype='application/atom+xml')

from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if not 'username' in request.POST:
        return HttpResponse('go to login cleantha')

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        print request.user
        return store_view(request)
    else:
        #验证失败，暂时不做处理
        return store_view(request)

def logout_view(request):
    logout(request)
    return store_view(request)