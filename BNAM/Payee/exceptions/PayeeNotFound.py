from rest_framework.exceptions import APIException
from rest_framework import status

class PayeeNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'PAYEE_NOT_FOUND'

    def __init__(self, payee_id=None):
        if payee_id is not None:
            detail = f'Payee with id {payee_id} not found.'
        else:
            detail = 'Payee Not Found'
        super().__init__(detail)
