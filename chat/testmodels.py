from django.test import TestCase
from django.http import HttpResponse
from .models import User, Room, ExtendedModel


class ExtendedModelTestCase(TestCase):

    TEST_USER_NICK = "picard"
    TEST_USER_AVATAR = "http://example.com"
    TEST_ROOM_NAME = "test room"

    def setUp(self):
        User.objects.create(nick=self.TEST_USER_NICK, avatar=self.TEST_USER_AVATAR)
        Room.objects.create(name=self.TEST_ROOM_NAME)

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

        # Get the test user
        test_user = User.objects.get(nick=self.TEST_USER_NICK)

        # Update the fields by keyword
        new_avatar = "http://newurl.com"
        test_user.update_data(avatar=new_avatar)

        # Verify that the avatar was updated
        self.assertEqual(test_user.avatar, new_avatar)

    def test_save_returns_http_response(self):

        # Create a conflicting test user
        duplicate_user = User(nick=self.TEST_USER_NICK, avatar=self.TEST_USER_AVATAR)

        # Attempt to save.  Internally this will throw, but it should get wrapped in an HttpResponse
        result = duplicate_user.save()

        self.assertIsInstance(result, HttpResponse)

    def test_delete_returns_http_response(self):

        # Get the test user
        test_user = User.objects.get(nick=self.TEST_USER_NICK)

        # Delete the test user, this should succeed, and return an HttpResponse
        result = test_user.delete()

        self.assertIsInstance(result, HttpResponse)

        # Previous delete cleared the id field.  Attempting to delete now will internally throw, but it should get
        # wrapped in an HttpResponse
        result = test_user.delete()

        self.assertIsInstance(result, HttpResponse)

        # Also try setting a bogus id and deleting
        test_user.id = 0
        result = test_user.delete()

        self.assertIsInstance(result, HttpResponse)
