from rest_framework.exceptions import APIException
from rest_framework import status

class CategoryGroupDoesNotBelongToBudget(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'CATEGORY_GROUP_DOES_NOT_BELONG_TO_BUDGET'

    def __init__(self, category_group_id=None, budget_id=None):
        if category_group_id is not None and budget_id is not None:
            detail = f'Category Group with ID {category_group_id} does not belong to Budget with ID {budget_id}'
        else:
            detail = 'Category Group does not belong budget'
        super().__init__(detail)
