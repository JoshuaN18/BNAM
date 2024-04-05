from rest_framework.exceptions import APIException
from rest_framework import status

class CategoryCannotBeNull(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Category cannot be null'
    default_code = 'CATEGORY_CANNOT_BE_NULL'