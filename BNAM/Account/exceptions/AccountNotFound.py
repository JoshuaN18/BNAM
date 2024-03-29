from rest_framework.exceptions import APIException
from rest_framework import status

class AccountNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'ACCOUNT_NOT_FOUND'

    def __init__(self, account_id=None):
        if account_id is not None:
            detail = f'Account with id {account_id} not found.'
        else:
            detail = 'Account Not Found'
        super().__init__(detail)
