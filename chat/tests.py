from django.db import models
from django.test import TestCase
from django.core.management import call_command

from chat.models import User, Room, ExtendedModel


class ExtendedModelTestCase(TestCase):

    TEST_USER_NICK = "picard"
    TEST_ROOM_NAME = "test room"

    def setUp(self):
        User(nick=self.TEST_USER_NICK, avatar="http://example.com").save()
        Room(name=self.TEST_ROOM_NAME).save()

    def test_no_whitelist(self):

        # Get the test user
        test_user = User.objects.get(nick=self.TEST_USER_NICK)

        # Verify that the test user does NOT override the white_list method.  If it does, find a new example model and
        # update this test please.
        self.assertEqual(test_user.white_list.__func__, ExtendedModel.white_list)

        # Verify that the test user whitelist returns ALL fields from the user object, the default behavior
        self.assertEqual(set(test_user.white_list()), set(test_user.to_data().keys()))

    def test_whitelist(self):

        # Get the test room
        test_room = Room.objects.get(name=self.TEST_ROOM_NAME)

        # Verify that the test room DOES override the white_list method.  If it doesn't, find a new example model and
        # update this test please.
        self.assertNotEqual(test_room.white_list.__func__, ExtendedModel.white_list)

        # Verify that the test room ONLY returns the fields from our white list, nothing more, nothing less.
        self.assertEqual(set(test_room.white_list()), set(test_room.to_data().keys()))

    def test_update_by_keyword(self):
        pass

    def test_save_returns_http_response(self):
        pass

    def test_delete_returns_http_response(self):
        pass
