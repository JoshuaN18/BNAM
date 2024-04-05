from rest_framework.exceptions import APIException
from rest_framework import status

class MonthlyCategoryNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'MONTHLY_CATEGORY_NOT_FOUND'

    def __init__(self, monthly_category_id=None):
        if monthly_category_id is not None:
            detail = f'Monthly Category with id {monthly_category_id} not found.'
        else:
            detail = 'Monthly Category Not Found'
        super().__init__(detail)
