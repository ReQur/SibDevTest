import logging

from typing import Union
from django.db import models

logger = logging.getLogger(__name__)


class DealSet(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    _cached_deals: Union[models.QuerySet, None] = None
    
    def save(
        self, **kwargs
    ):
        super().save(**kwargs)
        logger.info("New data saved. Clear cache")
        DealSet._cached_deals = None
        
    @classmethod
    def get_last(cls) -> models.QuerySet:
        if not cls._cached_deals:
            logger.info("No cached value. Information was got from DB")
            cls._cached_deals = Deal.objects.filter(
                deal_set=cls.objects.last()
            )
        logger.info("Found cached value. Passed")
        return cls._cached_deals


class Deal(models.Model):
    customer = models.CharField("customer", max_length=64)
    item = models.CharField("item", max_length=64)
    total = models.IntegerField("total")
    quantity = models.IntegerField("quantity")
    date = models.DateTimeField()
    deal_set = models.ForeignKey(DealSet, on_delete=models.CASCADE)
