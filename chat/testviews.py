from django.test import TestCase, Client
from json import dumps, loads
from .models import Room, User, Message


class ViewTestBase(TestCase):
    """ Shared helper functions for testing API views. """

    def setUp(self):
        """ Set up a django test client, and verify that we have an _endpoint attribute defined.

        The _endpoint class variable should be defined as the base url (i.e. "/api/users/") which all
        POST/GET/PUT/DELETE HTTP requests should be directed.  For requests that contain an item ID as part of the URL,
        this ID will be appended as needed.
        """
        self._client = Client()

        if not hasattr(self, '_endpoint'):
            raise NotImplementedError("Please specify an _endpoint member for your view test class")

    def _get_url_with_params(self, *args):
        if args:
            return self._endpoint + "/".join(map(str, args)) + "/"
        else:
            return self._endpoint

    def _create(self, *args, **kwargs):
        return self._client.post(self._get_url_with_params(*args), data=dumps(kwargs), content_type='application/json')

    def _read(self, *args, **kwargs):
        return self._client.get(self._get_url_with_params(*args), data=kwargs)

    def _update(self, *args, **kwargs):
        return self._client.put(self._get_url_with_params(*args), data=dumps(kwargs),
                                content_type='application/json')

    def _delete(self, *args):
        return self._client.delete(self._get_url_with_params(*args))


class UserViewTests(ViewTestBase):
    """ Test our user view. """
    _endpoint = "/api/users/"

    def test_post_bad_data(self):
        """ Test creating a user without all the required fields. """
        response = self._create(avatar="http://example.com")

        # Verify error status returned
        self.assertEqual(response.status_code, 400)

    def test_post_good_data(self):
        """ Test creating a user WITH all the required fields. """
        input_data = {"nick": "riker", "avatar": "http://example.com"}
        response = self._create(**input_data)

        # Verify created status returned
        self.assertEqual(response.status_code, 201)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the user we created contains AT LEAST the values we specified.  Likely the object will
        # contain more than that, because of calculated or defaulted fields.
        result_data_set = set(result_data.items())
        input_data_set = set(input_data.items())
        self.assertTrue(input_data_set.issubset(result_data_set))

    def test_get_all(self):
        """ Test creating multiple users and getting them all back at once. """
        self._create(nick="riker", avatar="http://example.com")
        self._create(nick="worf", avatar="http://newexample.com")

        # Read them all back
        response = self._read()

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that we got back a dictionary with "users" as a key
        self.assertIn("users", result_data)

        # Verify that the list contained in the "users" key is equal to the number of users we created (2).
        self.assertEqual(2, len(result_data["users"]))

    def test_get_one(self):
        """ Test creating a user and reading that user specifically. """
        new_user_response = self._create(nick="riker", avatar="http://example.com")

        # Deserialize response data so we can get the ID of the created user.
        new_user = loads(new_user_response.content.decode('utf-8'))

        # Attempt to read the same user by his/her ID
        response = self._read(new_user["id"])

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the user data returned from the creation EXACTLY matches the data we get by querying for
        # that same user directly
        self.assertDictEqual(new_user, result_data)

    def test_put(self):
        """ Test updating a user. """
        new_user_response = self._create(nick="riker", avatar="http://example.com")

        # Deserialize response data so we can get the ID of the created user.
        new_user = loads(new_user_response.content.decode('utf-8'))

        # Attempt to update the user's avatar
        new_avatar = "http://notexample.com"
        response = self._update(new_user["id"], avatar=new_avatar)

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the avatar field has been updated
        self.assertEqual(result_data["avatar"], new_avatar)

    def test_delete(self):
        """ Test deleting a user. """
        new_user_response = self._create(nick="riker", avatar="http://example.com")

        # Deserialize response data so we can get the ID of the created user.
        new_user = loads(new_user_response.content.decode('utf-8'))

        # Attempt to delete the user
        response = self._delete(new_user["id"])

        # Verify a no content status
        self.assertTrue(response.status_code, 204)

        # Attempt to read the user we just deleted
        response = self._read(new_user["id"])

        # Verify a not found status
        self.assertTrue(response.status_code, 404)


class RoomViewTests(ViewTestBase):
    """ Test our room view. """
    _endpoint = "/api/rooms/"

    def test_post_bad_data(self):
        """ Test creating a room without all the required fields. """
        response = self._create()

        # Verify error status returned
        self.assertEqual(response.status_code, 400)

    def test_post_good_data(self):
        """ Test creating a room WITH all the required fields. """
        input_data = {"name": "test chat room"}
        response = self._create(**input_data)

        # Verify created status returned
        self.assertEqual(response.status_code, 201)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the room we created contains AT LEAST the values we specified.  Likely the object will
        # contain more than that, because of calculated or defaulted fields.
        result_data_set = set(result_data.items())
        input_data_set = set(input_data.items())
        self.assertTrue(input_data_set.issubset(result_data_set))

    def test_get_all(self):
        """ Test creating multiple rooms and getting them all back at once. """
        self._create(name="enterprise")
        self._create(name="excelsior")

        # Read them all back
        response = self._read()

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that we got back a dictionary with "rooms" as a key
        self.assertIn("rooms", result_data)

        # Verify that the list contained in the "rooms" key is equal to the number of rooms we created (2).
        self.assertEqual(2, len(result_data["rooms"]))

    def test_get_one(self):
        """ Test creating a room and reading that room specifically. """
        new_room_response = self._create(name="engineering")

        # Deserialize response data so we can get the ID of the created room.
        new_room = loads(new_room_response.content.decode('utf-8'))

        # Attempt to read the same room by its ID
        response = self._read(new_room["id"])

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the room data returned from the creation EXACTLY matches the data we get by querying for
        # that same room directly
        self.assertDictEqual(new_room, result_data)

    def test_put(self):
        """ Test updating a room. """
        new_room_response = self._create(name="vulcan")

        # Deserialize response data so we can get the ID of the created room.
        new_room = loads(new_room_response.content.decode('utf-8'))

        # Attempt to update the room's name
        new_name = "romula"
        response = self._update(new_room["id"], name=new_name)

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the name field has been updated
        self.assertEqual(result_data["name"], new_name)

    def test_delete(self):
        """ Test deleting a room. """
        new_room_response = self._create(name="cardassia")

        # Deserialize response data so we can get the ID of the created room.
        new_room = loads(new_room_response.content.decode('utf-8'))

        # Attempt to delete the room
        response = self._delete(new_room["id"])

        # Verify a no content status
        self.assertTrue(response.status_code, 204)

        # Attempt to read the room we just deleted
        response = self._read(new_room["id"])

        # Verify a not found status
        self.assertTrue(response.status_code, 404)


class MessageViewTests(ViewTestBase):
    """ Test our message view. """
    _endpoint = "/api/"

    def setUp(self):
        """ For this test case, we'll need a room and a user pre-populated in the database. """
        super().setUp()

        # Create a test user and room that we can use to simulate messages.
        self.test_room = Room.objects.create(name="Enterprise")
        self.test_user = User.objects.create(nick="Picard", avatar="http://example.com")

        # Update our endpoint url to include the test room ID
        self._endpoint += "rooms/" + str(self.test_room.id) + "/messages/"

    def test_post_bad_data(self):
        """ Test creating a message without all the required fields. """
        response = self._create(msg="some message")

        # Verify error status returned
        self.assertEqual(response.status_code, 400)

    def test_post_good_data(self):
        """ Test creating a message WITH all the required fields. """
        input_data = {"room": self.test_room.id, "user": self.test_user.id, "msg": "test chat message"}
        response = self._create(**input_data)

        # Verify created status returned
        self.assertEqual(response.status_code, 201)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the message we created contains AT LEAST the values we specified.  Likely the object will
        # contain more than that, because of calculated or defaulted fields.
        result_data_set = set(result_data.items())
        input_data_set = set(input_data.items())
        self.assertTrue(input_data_set.issubset(result_data_set))

    def test_get_all(self):
        """ Test creating multiple messages and getting them all back at once. """
        self._create(room=self.test_room.id, user=self.test_user.id, msg="first message ever")
        self._create(room=self.test_room.id, user=self.test_user.id, msg="second message ever")

        # Read them all back
        response = self._read()

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that we got back a dictionary with "messages" as a key
        self.assertIn("messages", result_data)

        # Verify that the list contained in the "messages" key is equal to the number of messages we created (2).
        self.assertEqual(2, len(result_data["messages"]))

    def test_get_one(self):
        """ Test a message and reading it back individually. """
        new_message_response1 = self._create(room=self.test_room.id, user=self.test_user.id, msg="first message ever")

        # Deserialize response data so we can get the ID of the created message.
        new_message1 = loads(new_message_response1.content.decode('utf-8'))

        # Attempt to read all messages before the message with the specified ID
        response = self._read(new_message1["id"])

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that we got back the same message.
        self.assertDictEqual(new_message1, result_data)

    def test_get_previous(self):
        """ Test creating two messages and reading all messages prior to the first one (the second one basically). """
        new_message_response1 = self._create(room=self.test_room.id, user=self.test_user.id, msg="first message ever")
        new_message_response2 = self._create(room=self.test_room.id, user=self.test_user.id, msg="second message ever")

        # Deserialize response data so we can get the ID of the created message.
        new_message1 = loads(new_message_response1.content.decode('utf-8'))
        new_message2 = loads(new_message_response2.content.decode('utf-8'))

        # Attempt to read all messages before the message with the specified ID
        response = self._read(before=new_message2["id"])

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that we got back a dictionary with "messages" as a key
        self.assertIn("messages", result_data)

        # Verify that the list contained in the "messages" key is equal to one less than the number of messages we
        # created (1).
        self.assertEqual(1, len(result_data["messages"]))

        # Verify that we got back the older message of the two.
        self.assertDictEqual(new_message1, result_data["messages"][0])

    def test_put(self):
        """ Test updating a message. """
        new_message_response = self._create(room=self.test_room.id, user=self.test_user.id, msg="first message ever")

        # Deserialize response data so we can get the ID of the created message.
        new_message = loads(new_message_response.content.decode('utf-8'))

        # Attempt to update the message's name
        new_msg = "better not do this!"
        response = self._update(new_message["id"], msg=new_msg)

        # Verify an invalid request status (updates are not supported for messages)
        self.assertTrue(response.status_code, 400)

    def test_delete(self):
        """ Test deleting a message. """
        new_message_response = self._create(room=self.test_room.id, user=self.test_user.id, msg="first message ever")

        # Deserialize response data so we can get the ID of the created message.
        new_message = loads(new_message_response.content.decode('utf-8'))

        # Attempt to delete the message
        response = self._delete(new_message["id"])

        # Verify a no content status
        self.assertTrue(response.status_code, 204)

        # Attempt to read the message we just deleted
        response = self._read(new_message["id"])

        # Verify a not found status
        self.assertTrue(response.status_code, 404)


class MemberViewTests(ViewTestBase):
    """ Test our member view. """
    _endpoint = "/api/"

    def setUp(self):
        """ For this test case, we'll need a room and a user pre-populated in the database. """
        super().setUp()

        # Create a test user and room that we can use to simulate members.
        self.test_room = Room.objects.create(name="Enterprise")
        self.test_user1 = User.objects.create(nick="Picard", avatar="http://example.com")
        self.test_user2 = User.objects.create(nick="Riker", avatar="http://newexample.com")

        # Update our endpoint url to include the test room ID
        self._endpoint += "rooms/" + str(self.test_room.id) + "/members/"

    def test_post_bad_data(self):
        """ Test creating a member without all the required fields. """
        response = self._create()

        # Verify error status returned
        self.assertEqual(response.status_code, 400)

    def test_post_good_data(self):
        """ Test creating a member WITH all the required fields. """
        input_data = {"user": self.test_user1.id}
        response = self._create(**input_data)

        # Verify created status returned
        self.assertEqual(response.status_code, 201)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that the member we created is in the resulting member list
        self.assertIn("members", result_data)
        self.assertEqual(self.test_user1.id, result_data["members"][0]["id"])

    def test_get_all(self):
        """ Test creating multiple members and getting them all back at once. """
        self._create(user=self.test_user1.id)
        self._create(user=self.test_user2.id)

        # Read them all back
        response = self._read()

        # Verify an ok status
        self.assertTrue(response.status_code, 200)

        # Deserialize response data
        result_data = loads(response.content.decode('utf-8'))

        # Verify that we got back a dictionary with "members" as a key
        self.assertIn("members", result_data)

        # Verify that the list contained in the "members" key is equal to the number of members we created (2).
        self.assertEqual(2, len(result_data["members"]))

    def test_get_one(self):
        """ Test creating one member and attempting to read it back (not supported). """
        self._create(user=self.test_user1.id)

        # Attempt to read one member with the specified ID
        response = self._read(self.test_user1.id)

        # Verify a not found status (why would you want to read one member?)
        self.assertTrue(response.status_code, 400)

    def test_delete(self):
        """ Test deleting a member. """
        self._create(user=self.test_user1.id)

        # Attempt to delete the member
        response = self._delete(self.test_user1.id)

        # Verify a no content status
        self.assertTrue(response.status_code, 204)

        # Attempt to read the member we just deleted
        response = self._read(self.test_user1.id)

        # Verify a not found status
        self.assertTrue(response.status_code, 404)
