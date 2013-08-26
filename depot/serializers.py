# __author__ = 'cleantha'
from django.core.urlresolvers import reverse
from rest_framework.views import View
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework import serializers
from models import *


'''
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
        title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    imageUrl = models.URLField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    avalaibleData = models.DateField()

'''


class LineItemSerializer(ModelSerializer):
    class Meta:
        model = LineItem
        fields = ('product', 'product_title', 'order', 'unit_price', 'quantity')

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'imageUrl', 'price', 'avalaibleData')

