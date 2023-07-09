from django.db import models


class DealSet(models.Model):
    date = models.DateTimeField(auto_now_add=True)


class Deal(models.Model):
    customer = models.CharField('customer', max_length=64)
    item = models.CharField('item', max_length=64)
    total = models.IntegerField('total')
    quantity = models.IntegerField('quantity')
    date = models.DateTimeField()
    deal_set = models.ForeignKey(DealSet, on_delete=models.CASCADE)
