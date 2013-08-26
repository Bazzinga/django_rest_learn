# -*- coding: utf-8 -*-

from django import forms
from models import *

from django import forms
from models import *

import itertools

def anyTrue(predicate, sequence):
    return True in itertools.imap(predicate, sequence)
def endsWith(s, *endings):
    return anyTrue(s.endswith, endings)

def validateImageUrl(url, suffixlist):
    for suffix in suffixlist:
        if str(url).endswith(str(suffix)):
            return True
    return False

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_order(self):
        order = self.cleaned_data['order']
        return order

    def clean_price(self):
        price = self.cleaned_data['price']
        # print type(price)
        if price <= 0:
            raise forms.ValidationError("价格必须大于零")
        return price

    def clean_imageUrl(self):
        url = self.cleaned_data['imageUrl']
        print str(url)
        # print type(url)
        if not endsWith(url.lower(), '.jpg', '.png', '.gif', '.jpg/', '.png/', '.gif/'):
            raise forms.ValidationError('图片格式必须为jpg、png或gif')
        # if not validateImageUrl(str(url), ['.jpg/', '.png/', '.gif/']):
        #     raise forms.ValidationError('图片格式必须为jpg、png或gif')
        return url

class OrderForm(forms.ModelForm):
	
    class Meta:
        model = Order	
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

