import io
import logging
import csv

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deal

logger = logging.getLogger(__name__)

TEXT_CSF_FILETYPE = "text/csv"
class PostTableView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_id='Upload deals table',
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Deals table to be uploaded'),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                'Success'
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "Failure: File expected"
            ),
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: openapi.Response(
                "Failure: Got file that isn't .csv format"
            ),
        }
    )
    def post(self, request):
        file_obj = request.FILES['file']
        file_type = file_obj.content_type
        logger.info(f"got file with type: {file_type}")
        if file_type != TEXT_CSF_FILETYPE:
            return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, exception=True)
        if not file_obj:
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data="File expected")

        decoded_file = file_obj.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)

        _reader = csv.reader(io_string, delimiter=',')
        # skip header
        _reader.__next__()
        for line in _reader:
            logger.info(line)
            deal = Deal()
            deal.customer = line[0]
            deal.item = line[1]
            deal.total = int(line[2])
            deal.quantity = int(line[3])
            deal.date = line[4]
            deal.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class GetTopCustomers(APIView):
    @swagger_auto_schema(
        operation_id='Get the most spent users',
        operation_description='Get list of 5 clients who spent the largest amount for the entire period.',
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Success', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='user name'),
                    'spent_money': openapi.Schema(type=openapi.TYPE_STRING, description='amount of money spent in entire period'),
                    'gems': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of gems',
                                           items=openapi.Schema(type=openapi.TYPE_STRING, description='Gem name'))
                })
            )
        }
    )
    def get(self, request):
        pass