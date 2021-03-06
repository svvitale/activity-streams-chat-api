from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .decorators import json, room_stream_subscriber, room_stream_publisher
from .models import Room, User, Message


class CRUDView(View):
    """Base view class that implements default versions of the primary HTTP verbs (POST, GET, PUT, DELETE).

    All verb implementations expect to receive and return dictionary objects.  All serialization/deserialization
    is handled outside of the view itself.
    """

    @json
    def post(self, json_data, *args, **kwargs):
        """ POST verb handler (database create).  Only supports single item creation at this time.
        :param json_data: Model attributes to use in the creation of a new database entry.
        :return: Public representation of the created model.  This may not include all model fields, depending
                on how the model defines its to_data() member.
        """
        return self._model(**json_data).save()

    @json
    def get(self, json_data, item_id=None, *args, **kwargs):
        """ GET verb handler (database read)
        :param json_data: Not used.
        :param item_id: (optional) Unique ID of the object to retrieve.  If not specified, all objects will be returned.
        :return: Public representation of the requested object (if item_id specified) or a dictionary containing a
                single key referencing a list of public representations of all available objects in this collection.
        """
        if item_id:
            return get_object_or_404(self._model, id=item_id).to_data()
        else:
            return {
                self._collection_name: [item_obj.to_data() for item_obj in self._model.objects.all()]
            }

    @json
    def put(self, json_data, item_id, *args, **kwargs):
        """ PUT verb handler (database update).  Only supports single item updates at this time.
        :param json_data: Dictionary of key/value pairs that should be updated on the specified object
        :param item_id: Unique ID of the object to update.
        :return: Public representation of the updated object
        """
        existing_item = get_object_or_404(self._model, id=item_id)
        existing_item.update_data(**json_data)
        return existing_item.save()

    @json
    def delete(self, json_data, item_id, *args, **kwargs):
        """ DELETE verb handler (database delete).  Only supports single item deletions at this time.
        :param json_data: Not used.
        :param item_id: Unique ID of the object to delete.
        :return: Status 204 on success, error message on failure
        """
        existing_item = get_object_or_404(self._model, id=item_id)
        return existing_item.delete()


class RoomView(CRUDView):
    """ View for the Room model.  Uses the default CRUDView implementation. """
    _model = Room
    _collection_name = "rooms"


class UserView(CRUDView):
    """ View for the User model.  Uses the default CRUDView implementation. """
    _model = User
    _collection_name = "users"


class MessageView(View):
    """ View for the Message model.  Needs to retrieve 50 messages at a time, and no support for updates. """
    @staticmethod
    def _stream_name(room_id):
        return 'messages-' + room_id

    @room_stream_publisher
    @json
    def post(self, json_data, room_id):
        """ Add a new message to the specified room.
        :param json_data: Message data to create
        :param room_id: Unique ID of the room to which we're adding the message
        :return: Message data
        """
        json_data["room"] = get_object_or_404(Room, id=room_id)

        if "user" not in json_data:
            return HttpResponse("User is a required field", status=400)

        json_data["user"] = get_object_or_404(User, id=json_data["user"])
        return Message.objects.create(**json_data).to_data()

    @room_stream_subscriber
    @json
    def get(self, json_data, room_id, item_id=None, *args, **kwargs):
        """
        :param json_data: Not used.
        :param room_id: Unique ID of the room from which we're retrieving messages.
        :param item_id: (optional) If specified, return the message with this item_id.
        :return:
        """
        room = get_object_or_404(Room, id=room_id)

        # Return just the message specified
        if item_id:
            msg = get_object_or_404(Message, id=item_id, room=room)
            return msg.to_data()

        if "before" in json_data:
            msg = get_object_or_404(Message, id=json_data["before"])
        else:
            msg = None

        # Return the last 50 messages from this room
        return room.messages(since_msg=msg, msg_count=50)

    def put(self, *args, **kwargs):
        """ Message updates are not supported. """
        return HttpResponse("Unsupported verb: PUT", status=400)


class MemberView(View):

    @staticmethod
    def _stream_name(room_id):
        return 'members-' + room_id

    @room_stream_publisher
    @json
    def post(self, json_data, room_id):
        """ Add a member to the specified room.
        :param json_data: Dictionary containing at least "user_id" as a key
        :return: Public representation of this room's member list.
        """
        # Load up the specified room
        room = get_object_or_404(Room, id=room_id)

        # Ensure user_id was specified
        if "user" not in json_data:
            return HttpResponse("user is required", status=400)

        # Load up the specified user
        user = get_object_or_404(User, id=json_data["user"])

        # Return an error if this user already existing in the room
        if user in room.members.all():
            return HttpResponse("User is already a member of this room", status=409)

        # Add the user to the room, save, and return
        room.members.add(user)
        room.save()

        return room.member_data()

    @room_stream_subscriber
    @json
    def get(self, json_data, room_id, user_id=None):
        """ Get the list of members in the specified room.
        :param json_data: Not used.
        :param room_id: Room to get members from.
        :return: Object with a list of members in the specified room.
        """
        if user_id:
            return HttpResponse("Reading a specific member is not supported", status=400)

        room = get_object_or_404(Room, id=room_id)
        return room.member_data()

    def put(self, *args, **kwargs):
        """ Member updates are not supported. """
        return HttpResponse("Unsupported verb: PUT", status=400)

    @room_stream_publisher
    @json
    def delete(self, json_data, room_id, user_id):
        """ Remove a user from the specified room
        :param json_data: Not used.
        :param room_id: Room from which to remove the user
        :param user_id: User to remove
        :return: Status 204 on success, error message on failure
        """
        room = get_object_or_404(Room, id=room_id)
        user = get_object_or_404(User, id=user_id)

        if user not in room.members.all():
            return HttpResponse("User is not a member of this room", status=400)

        # Remove the user from the room, save, and return
        room.members.remove(user)
        room.save()

        return user.to_data()
