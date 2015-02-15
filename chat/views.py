from django.views.generic import View
from django.shortcuts import get_object_or_404

from chat.decorators import json
from chat.models import Room, User, Message


class BaseView(View):

    @json
    def post(self, json_data):
        return self._model(**json_data).save()

    @json
    def get(self, json_data, item_id=None):

        if item_id:
            return get_object_or_404(self._model, id=item_id).to_data()
        else:
            return {
                self._collection_name: [item_obj.to_data() for item_obj in self._model.objects.all()]
            }

    @json
    def put(self, json_data, item_id):
        existing_item = get_object_or_404(self._model, id=item_id)
        existing_item.update_data(**json_data)
        return existing_item.save()

    @json
    def delete(self, item_id):
        existing_item = get_object_or_404(self._model, id=item_id)
        return existing_item.delete()


class RoomView(BaseView):
    _model = Room
    _collection_name = "rooms"


class UserView(BaseView):
    _model = User
    _collection_name = "users"


class MessageView(BaseView):
    _model = Message
    _collection_name = "messages"

    @json
    def get(self, json_data, item_id=None):

        if item_id:
            starting_msg = get_object_or_404(self._model, id=item_id)
            query_set = self._model.objects.filter(timestamp__lt=starting_msg.timestamp)
        else:
            query_set = self._model.objects.all()

        return {
            self._collection_name: [item_obj.to_data() for item_obj in query_set.order_by('-timestamp')[:50]]
        }
