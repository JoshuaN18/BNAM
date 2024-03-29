from rest_framework.exceptions import APIException
from rest_framework import status

class CategoryGroupNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'CATEGORY_GROUP_NOT_FOUND'

    def __init__(self, category_group_id=None):
        if category_group_id is not None:
            detail = f'Category Group with id {category_group_id} not found.'
        else:
            detail = 'Category Group Not Found'
        super().__init__(detail)
