from rest_framework.exceptions import APIException
from rest_framework import status

class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'USER_NOT_FOUND'

    def __init__(self, user_id=None):
        if user_id is not None:
            detail = f'User with id {user_id} not found.'
        else:
            detail = 'User Not Found'
        super().__init__(detail)
