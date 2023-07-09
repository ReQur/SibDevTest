from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deal

# Create your views here.

#FILE = openapi.Parameter('test', openapi.IN_BODY, description="CSV file with deals data", type=openapi.TYPE_FILE)

class PostTableView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_id='Upload deals table',
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Deals table to be uploaded'),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                'Success', schema=openapi.Schema(type=openapi.TYPE_OBJECT)
            )
        }
    )
    def post(self, request):
        file_obj = request.FILES['file']
        # do some stuff with uploaded file
        if file_obj:
            return Response(status=204)