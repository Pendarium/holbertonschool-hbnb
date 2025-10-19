import unittest
from app.services.facade import HBnBFacade


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()
        self.user = self.facade.create_user({
            "first_name": "John", "last_name":
            "Doe", "email": "john@example.com"
        })

    def test_create_place_valid(self):
        data = {
            "title": "Nice place",
            "description": "A lovely place",
            "price": 100.0,
            "latitude": 10,
            "longitude": 20,
            "owner_id": self.user.id,
            "amenities": []
        }
        place = self.facade.create_place(data)
        self.assertEqual(place.title, "Nice place")
        self.assertEqual(place.owner.id, self.user.id)

    def test_create_place_invalid_price(self):
        data = {
            "title": "Place",
            "price": -50,
            "latitude": 10,
            "longitude": 20,
            "owner_id": self.user.id,
            "amenities": []
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(data)

    def test_create_place_invalid_latitude(self):
        data = {
            "title": "Place",
            "price": 50,
            "latitude": 100,
            "longitude": 20,
            "owner_id": self.user.id,
            "amenities": []
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(data)


if __name__ == "__main__":
    unittest.main()
