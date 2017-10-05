"""Test cases to unit test client.py."""
import client
import unittest
import mock


"""Following function is used to mock responses
   when a particular URL is called.
"""


def mocked_request(*args, **kwargs):
    if args[0] == "http://127.0.0.1:5000/register":
        return {"register_method": 200}

    elif args[0] == "http://127.0.0.1:5000/allemployees":
        return {"get_method": 200}

    elif args[0] == "http://127.0.0.1:5000/checkemp":
        return {"check_employee_method": 200}

    elif args[0] == "http://127.0.0.1:5000/updateemp":
        return {"update_method": 200}

    elif args[0] == "http://127.0.0.1:5000/deleteemp":
        return {"delete_method": 200}

    else:
        return {"method": "Not Found"}


class TestClient(unittest.TestCase):
    """Mocking the call to REST API by replacing
       requests.post with mocked_request method.
    """
    @mock.patch("requests.post", side_effect=mocked_request)
    def test_register(self, m):
        json_data = client.register()
        self.assertEquals(json_data, {"register_method": 200})

    """Mocking the call to REST API by replacing
       requests.get with mocked_request method.
    """
    @mock.patch("requests.get", side_effect=mocked_request)
    def test_display(self, m):
        json_data = client.display()
        self.assertEquals(json_data, {"get_method": 200})

    """Mocking the call to REST API by replacing
       requests.get with mocked_request method.
    """
    @mock.patch("requests.get", side_effect=mocked_request)
    def test_check_employee(self, m):
        json_data = client.check_employee()
        self.assertEquals(json_data, {"check_employee_method": 200})

    """Mocking the call to REST API by replacing
       requests.put with mocked_request method.
    """
    @mock.patch("requests.put", side_effect=mocked_request)
    def test_update(self, m):
        json_data = client.update(1)
        self.assertEquals(json_data, {"update_method": 200})

    """Mocking the call to REST API by replacing
       requests.delete with mocked_request method.
    """
    @mock.patch("requests.delete", side_effect=mocked_request)
    def test_delete(self, m):
        json_data = client.delete()
        self.assertEquals(json_data, {"delete_method": 200})


"""Executing the test cases."""
if __name__ == "__main__":
    unittest.main()

