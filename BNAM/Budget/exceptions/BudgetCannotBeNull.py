from rest_framework.exceptions import APIException
from rest_framework import status

class BudgetCannotBeNull(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Budget cannot be null'
    default_code = 'BUDGET_CANNOT_BE_NULL'