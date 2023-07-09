import io
import logging
import csv

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from django.db.models import Sum, Count

from .models import Deal
from .utils import fill_new_deal_set

logger = logging.getLogger(__name__)

TEXT_CSF_FILETYPE = "text/csv"


class PostTableView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_id="Upload deals table",
        manual_parameters=[
            openapi.Parameter(
                "file",
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Deals table to be uploaded",
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("Success"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "Failure: File expected"
            ),
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: openapi.Response(
                "Failure: Got file that isn't .csv format"
            ),
        },
    )
    def post(self, request):
        file_obj = request.FILES["file"]
        file_type = file_obj.content_type
        logger.info(f"got file with type: {file_type}")
        if file_type != TEXT_CSF_FILETYPE:
            return Response(
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, exception=True
            )
        if not file_obj:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                exception=True,
                data="File expected",
            )

        decoded_file = file_obj.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)

        _reader = csv.reader(io_string, delimiter=",")
        # skip header
        _reader.__next__()
        fill_new_deal_set(_reader)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GetTopCustomers(APIView):
    @swagger_auto_schema(
        operation_id="Get the most spent users",
        operation_description="Get list of 5 clients who spent "
                              "the largest amount for the entire period.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "response": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "username": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "spent_money": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                    "gems": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Gem name",
                                        ),
                                    ),
                                },
                            ),
                        )
                    },
                ),
            )
        },
    )
    def get(self, request):
        # Get the top 5 customers who spent
        #   the most money for the entire period
        top_5_customers = (
            Deal.objects.values("customer")
            .annotate(spent_money=Sum("total"))
            .order_by("-spent_money")[:5]
        )

        # Get the list of gems that were bought by
        #   at least two customers from the top 5 customers,
        #   and the current customer is one of them
        gem_list = (
            Deal.objects.filter(
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
                Deal.objects.filter(
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
        response = {"response": response_data}
        return Response(status=status.HTTP_200_OK, data=response)
