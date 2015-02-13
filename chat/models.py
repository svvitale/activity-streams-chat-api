from django.db import models


class User(models.Model):
    """ A global user within the chat system. """
    nick = models.CharField("user nickname", max_length=100, unique=True)
    avatar = models.URLField("avatar url", max_length=512)
    last_seen = models.DateTimeField("last time the user logged in", auto_now_add=True)


class Room(models.Model):
    """ A chat room. """
    name = models.CharField("room name", max_length=100, unique=True)
    members = models.ManyToManyField(User)


class Message(models.Model):
    """ An individual message in a chat room. """
    room = models.ForeignKey(Room)
    user = models.ForeignKey(User)
    msg = models.CharField("message text", max_length=4000)
    timestamp = models.DateTimeField("time message sent", auto_now_add=True)

