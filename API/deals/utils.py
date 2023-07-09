import logging

from functools import cache
from django.db import transaction
from django.db.models import Count, Sum, QuerySet

from .models import DealSet, Deal

logger = logging.getLogger(__name__)


@transaction.atomic()
def fill_new_deal_set(deals_iter) -> None:
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



@cache
def process_top_customers(deals: QuerySet) -> list[dict]:
    logger.info("Process top customers with new deals query set")
    # Get the top 5 customers who spent
    #   the most money for the entire period
    top_5_customers = (
        deals.values("customer")
        .annotate(spent_money=Sum("total"))
        .order_by("-spent_money")[:5]
    )

    # Get the list of gems that were bought by
    #   at least two customers from the top 5 customers,
    #   and the current customer is one of them
    gem_list = (
        deals.filter(
            customer__in=[c["customer"] for c in top_5_customers]
        )
        .values("item")
        .annotate(customer_count=Count("customer", distinct=True))
        .filter(customer_count__gte=2)
        .values_list("item", flat=True)
    )

    # Form the response
    response_data = []
    for customer in top_5_customers:
        # Get the list of gems bought by this customer
        customer_gems = (
            deals.filter(
                customer=customer["customer"], item__in=gem_list
            )
            .values_list("item", flat=True)
            .distinct()
        )

        # Add the customer and their data to the response
        response_data.append(
            {
                "username": customer["customer"],
                "spent_money": customer["spent_money"],
                "gems": list(customer_gems),
            }
        )

    return response_data
