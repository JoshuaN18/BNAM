from rest_framework.exceptions import APIException
from rest_framework import status

class CategoryNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'CATEGORY_NOT_FOUND'

    def __init__(self, category_id=None):
        if category_id is not None:
            detail = f'Category with id {category_id} not found.'
        else:
            detail = 'Category Not Found'
        super().__init__(detail)
