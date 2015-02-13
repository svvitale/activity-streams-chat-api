from django.http import JsonResponse


def json(view_func):
    def wrapper(*args, **kwargs):
        # Translate all returns into JsonResponses.  This allows us to return native Python data structures
        # without having to remember to Responsify it.
        return JsonResponse(view_func(*args, **kwargs))
    return wrapper
