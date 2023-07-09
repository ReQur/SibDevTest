import logging

from django.db import transaction

from .models import DealSet, Deal

logger = logging.getLogger(__name__)

@transaction.atomic()
def fill_new_deal_set(deals_iter):
    deal_set = DealSet()
    deal_set.save()

    for line in deals_iter:
        logger.debug(line)
        deal = Deal()
        deal.customer = line[0]
        deal.item = line[1]
        deal.total = int(line[2])
        deal.quantity = int(line[3])
        deal.date = line[4]
        deal.deal_set = deal_set
        deal.save()
