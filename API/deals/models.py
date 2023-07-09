from django.db import models

class Deal(models.Model):
    customer = models.CharField('customer', max_length=64)
    item = models.CharField('item', max_length=64)
    total = models.IntegerField('total')
    quantity = models.IntegerField('quantity')
    date = models.DateTimeField()

