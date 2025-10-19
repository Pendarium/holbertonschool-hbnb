import unittest
from app.services.facade import HBnBFacade


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()

    def test_create_user_valid(self):
        data = {"first_name": "John", "last_name":
                "Doe", "email": "john@example.com"}
        user = self.facade.create_user(data)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")

    def test_create_user_invalid_email(self):
        data = {"first_name": "John", "last_name":
                "Doe", "email": "invalid-email"}
        with self.assertRaises(ValueError):
            self.facade.create_user(data)

    def test_create_user_empty_fields(self):
        data = {"first_name": "", "last_name": "", "email": "john@example.com"}
        with self.assertRaises(ValueError):
            self.facade.create_user(data)

    def test_get_user_not_found(self):
        self.assertIsNone(self.facade.get_user("non-existent-id"))


if __name__ == "__main__":
    unittest.main()
