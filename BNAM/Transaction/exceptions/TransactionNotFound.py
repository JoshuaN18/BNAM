from rest_framework.exceptions import APIException
from rest_framework import status

class TransactionNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'TRANSACTION_NOT_FOUND'

    def __init__(self, transaction_id=None):
        if transaction_id is not None:
            detail = f'Transaction with id {transaction_id} not found.'
        else:
            detail = 'Transaction Not Found'
        super().__init__(detail)
