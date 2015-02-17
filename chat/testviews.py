from django.test import TestCase, Client
from json import dumps, loads


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

    def _create(self, *args, **kwargs):
        return self._client.post(self._endpoint, data=dumps(kwargs), content_type='application/json')

    def _read(self, user_id=None):
        if user_id:
            return self._client.get(self._endpoint + ("%s/" % (str(user_id),)))
        else:
            return self._client.get(self._endpoint)

    def _update(self, user_id, *args, **kwargs):
        return self._client.put(self._endpoint + ("%s/" % (str(user_id))), data=dumps(kwargs),
                                content_type='application/json')

    def _delete(self, user_id):
        return self._client.delete(self._endpoint + ("%s/" % (str(user_id))))


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
