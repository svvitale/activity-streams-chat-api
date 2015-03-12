from django.http import JsonResponse, HttpResponse
from json import loads
from gripcontrol import HttpStreamFormat
from django_grip import set_hold_stream, publish


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


def room_stream_subscriber(view_func):
    def wrapper(self, request, room_id, *args, **kwargs):
        """ Check if browser is attempting to subscribe to an event stream. """
        if request.META.get('HTTP_ACCEPT') == 'text/event-stream':
            set_hold_stream(request, self._stream_name(room_id))
            return HttpResponse(content_type='text/event-stream')

        return view_func(self, request, room_id, *args, **kwargs)

    return wrapper


def room_stream_publisher(view_func):
    def wrapper(self, request, room_id, *args, **kwargs):
        """ Automatically push the data returned from view_func. """

        response = view_func(self, request, room_id, *args, **kwargs)

        # If we got a JSON response, we'll want to publish this out
        if isinstance(response, JsonResponse):
            if request.method == 'POST':
                event = "create"
            elif request.method == 'DELETE':
                event = "delete"
            else:
                event = "update"

            # Got back a data object that needs to be published
            update_content = [HttpStreamFormat('event: %s\ndata: %s\n\n' % (event, response.content))]
            publish(self._stream_name(room_id), update_content)

        return response

    return wrapper
