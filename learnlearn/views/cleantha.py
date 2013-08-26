# __author__ = 'cleantha'

from django.http import HttpResponse

def cleantha(request):
    return HttpResponse('hello cleantha')