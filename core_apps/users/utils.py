from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        customized_response = {}
        
        customized_response_list = []
        

        for key, value in response.data.items():
            if isinstance(value,list) and len(value)==1:
                value = value[0]
            error = {'field': key, 'text': value}
            customized_response_list.append(error)
        
        if len(customized_response_list)==1:
            customized_response = customized_response_list[0]
        
        customized_response['status_code'] = response.status_code
        response.data = customized_response

    return response