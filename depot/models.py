from django.db import models

# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bookorder'

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    imageUrl = models.URLField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    avalaibleData = models.DateField()
    # dynamic add this after commit the shopping list
    # order = models.ManyToManyField(Order, through='LineItem', blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'product'

class LineItem(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    product_title = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'lineitem'

    def __unicode__(self):
        return Product.title

class Cart(object):

    def __init__(self):
        self.items = []
        self.totalprice = 0

    def add_product(self, product):
        self.totalprice += product.price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
                return
        self.items.append(LineItem(product=product, product_title=product.title, unit_price=product.price, quantity=1))