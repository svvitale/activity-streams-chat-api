from django.views.generic import View
from chat.decorators import json

from chat.models import Room
from django.forms import model_to_dict


class RoomView(View):

    @json
    def get(self, request):
        return {
            "rooms": [model_to_dict(x) for x in Room.objects.all()]
        }
