from django.db import models
from django.forms import model_to_dict
import django.db
from django.http import HttpResponse


class ExtendedModel(models.Model):

    def update_data(self, *args, **kwargs):
        """  Update this object's data from the keyword arguments passed in.  This only updates the object in memory,
        a call to save() is still required to persist the object to the database.
        """
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def save(self, *args, **kwargs):
        try:
            super().save(self, *args, **kwargs)
            return self.to_data()
        except django.db.IntegrityError as ex:
            return HttpResponse(str(ex), status=409)
        except django.db.Error as ex:
            return HttpResponse(str(ex), status=400)

    def delete(self, *args, **kwargs):
        super().delete(self, *args, **kwargs)
        return HttpResponse(status=200)

    def white_list(self):
        """ Whitelisted fields for this model.  By default, all fields are whitelisted.  Override this function
        to return only a subset of fields from an API call.
        """
        return self._meta.get_all_field_names()

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
        abstract = True


class User(ExtendedModel):
    """ A global user within the chat system. """
    nick = models.CharField("user nickname", max_length=100, unique=True)
    avatar = models.URLField("avatar url", max_length=512)
    last_seen = models.DateTimeField("last time the user logged in", auto_now_add=True)


class Room(ExtendedModel):
    """ A chat room. """
    name = models.CharField("room name", max_length=100, unique=True)
    members = models.ManyToManyField(User, blank=True)

    def white_list(self):
        # Only these fields will be returned by API calls
        return [
            'id',
            'name'
        ]


class Message(ExtendedModel):
    """ An individual message in a chat room. """
    room = models.ForeignKey(Room)
    user = models.ForeignKey(User)
    msg = models.CharField("message text", max_length=4000)
    timestamp = models.DateTimeField("time message sent", auto_now_add=True)

    def before(self, msg_id):
        """ Return the 50 messages prior to the passed message id.
        """
        pass