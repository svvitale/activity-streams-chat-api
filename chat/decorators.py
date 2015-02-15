from django.http import JsonResponse, HttpResponse
from json import loads


def json(view_func):
    def wrapper(self, request, *args, **kwargs):
        # Deserialize the request body into a native dictionary
        if request.body:
            json_data = loads(request.body.decode('utf-8'))
        else:
            json_data = {}

        # Call the view handler
        response = view_func(self, json_data, *args, **kwargs)

        # Translate the return into a JsonResponse if necessary.  This allows us to return native Python
        # data structures without having to remember to jsonify it.
        if isinstance(response, HttpResponse):
            return response
        else:
            return JsonResponse(response)

    return wrapper
