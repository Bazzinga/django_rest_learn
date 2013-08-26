# __author__ = 'cleantha'
from django.shortcuts import render_to_response

from django.http import HttpResponse

def hello(request):
    return HttpResponse("hello")

def show(request):
    return render_to_response('productlist.html', {})