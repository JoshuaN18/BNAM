from rest_framework.exceptions import APIException
from rest_framework import status

class BudgetNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'BUDGET_NOT_FOUND'

    def __init__(self, budget_id=None):
        if budget_id is not None:
            detail = f'Budget with id {budget_id} not found.'
        else:
            detail = 'Budget Not Found'
        super().__init__(detail)
