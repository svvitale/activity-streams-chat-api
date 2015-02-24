from django.http import JsonResponse, HttpResponse
from json import loads


def json(view_func):
    def wrapper(self, request, *args, **kwargs):
        # Deserialize the request body into a native dictionary
        if request.method == "GET":
            json_data = {k: v for k, v in request.GET.items()}
        elif request.body:
            json_data = loads(request.body.decode('utf-8'))
        else:
            json_data = {}

        # Call the view handler
        response = view_func(self, json_data, *args, **kwargs)

        # Translate the return into a JsonResponse if necessary.  This allows us to return native Python
        # data structures without having to remember to jsonify it.
        if isinstance(response, HttpResponse):
            # Most likely an error response.  Just pass it through
            return response
        else:
            # Return the appropriate HTTP status
            if request.method == "POST":
                status = 201
            elif request.method == "DELETE":
                status = 204
            else:
                status = 200

            return JsonResponse(response, status=status)

    return wrapper
