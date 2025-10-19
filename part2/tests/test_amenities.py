import unittest
from app.services.facade import HBnBFacade


class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()

    def test_create_amenity_valid(self):
        data = {"name": "WiFi"}
        amenity = self.facade.create_amenity(data)
        self.assertEqual(amenity.name, "WiFi")

    def test_create_amenity_empty_name(self):
        data = {"name": ""}
        with self.assertRaises(ValueError):
            self.facade.create_amenity(data)


if __name__ == "__main__":
    unittest.main()
