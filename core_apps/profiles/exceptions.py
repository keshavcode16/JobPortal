from rest_framework.exceptions import APIException


class ProfileDoesNotExist(APIException):
    """
    This class is for handling exception error 
    for a profile that does not exist
    """

    status_code = 400
    default_detail = 'The requested profile does not exist.'


class PostThreadDoesNotExist(APIException):
    """
    This class is for handling exception error 
    for a post thread that does not exist
    """

    status_code = 400
    default_detail = 'The requested post thread not found.'

