from django.db import models
from django.forms import model_to_dict
import django.db
from django.http import HttpResponse
from datetime import datetime


class ExtendedModel(models.Model):
    """ Extension of the Django model.Model class aimed at wrapping model data and database error conditions in more
    Restful responses.  Also supports whitelisting of model fields for easy filtering of public representations.
    """

    def update_data(self, *args, **kwargs):
        """  Update this object's data from the keyword arguments passed in.  This only updates the object in memory,
        a call to save() is still required to persist the object to the database.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self, *args, **kwargs):
        """ Save this object to the database and return its public representation.  Return appropriate HTTP status codes
        on error.
        """
        try:
            # Call the models.Model save method, passing along any positional or named arguments
            super().save(*args, **kwargs)

            # Return the save object's public representation
            return self.to_data()

        except django.db.IntegrityError as ex:
            # Foreign or unique key error
            if "violates not-null" in str(ex):
                return HttpResponse(str(ex), status=400)
            else:
                return HttpResponse(str(ex), status=409)

        except django.db.Error as ex:
            # General database error
            return HttpResponse(str(ex), status=400)

    def delete(self, *args, **kwargs):
        """ Delete this object from the database.  Return appropriate HTTP status codes on error. """
        try:
            # Call the models.Model delete method, passing along any positional or named arguments
            super().delete(*args, **kwargs)

            # Return the data that was deleted
            return self.to_data()

        except django.db.Error as ex:
            # General database error
            return HttpResponse(str(ex), status=400)

        except AssertionError as ex:
            # Django error such as "object can't be deleted because its id attribute is set to None"
            return HttpResponse(str(ex), status=400)

    def white_list(self):
        """ Whitelisted fields for this model.  By default, all fields are whitelisted.  Override this function
        to return only a subset of fields from an API call.
        """
        return [field.name for field in self._meta.fields]

    def to_data(self):
        """ Iterate over all attributes and return a native Python dictionary containing only the whitelisted
        attributes
        """
        data = {}

        # Retrieve our white list
        white_list = self.white_list()

        # Iterate over each of our fields and return a dictionary that contains only whitelisted fields.
        for attr_name, attr_val in model_to_dict(self).items():
            if attr_name in white_list:
                data[attr_name] = attr_val

        return data

    class Meta:
        """ Don't create this class in the database, it's not a true model. """
        abstract = True


def get_now():
    return datetime.utcnow()


class User(ExtendedModel):
    """ A global user within the chat system. """
    nick = models.CharField("user nickname", max_length=100, unique=True, default=None)
    avatar = models.URLField("avatar url", max_length=512, default=None, blank=True)
    last_seen = models.DateTimeField("last time the user logged in", default=get_now)


class Room(ExtendedModel):
    """ A chat room. """
    name = models.CharField("room name", max_length=100, unique=True, default=None)
    members = models.ManyToManyField(User, blank=True)

    def white_list(self):
        """ Whitelist override
        :return: List of fields to be included in API call responses.
        """
        return [
            'id',
            'name'
        ]

    def member_data(self):
        """ Return the member data as a json-serializable object. """
        return {
            "members": [member.to_data() for member in self.members.all()]
        }

    def messages(self, since_msg=None, msg_count=50):
        """ Return set of messages from this room ordered by timestamp
        :param since_msg: If specified, only get messages older than this message
        :param msg_count: If specified, return this number of messages (defaults to 50)
        :return: JSON-serializable object with "messages" key
        """
        if since_msg:
            query_set = Message.objects.filter(timestamp__lt=since_msg.timestamp, room=self)
        else:
            query_set = Message.objects.filter(room=self)

        return {
            "messages": [item_obj.to_data() for item_obj in query_set.order_by('-timestamp')[:msg_count]]
        }


class Message(ExtendedModel):
    """ An individual message in a chat room. """
    room = models.ForeignKey(Room, blank=False)
    user = models.ForeignKey(User, blank=False)
    msg = models.CharField("message text", max_length=4000, blank=False, default=None)
    timestamp = models.DateTimeField("time message sent", default=get_now)
