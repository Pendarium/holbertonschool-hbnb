import unittest
from app.services.facade import HBnBFacade


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()
        self.user = self.facade.create_user({
            "first_name": "John", "last_name":
            "Doe", "email": "john@example.com"
        })
        self.place = self.facade.create_place({
            "title": "Nice place",
            "description": "A lovely place",
            "price": 100,
            "latitude": 10,
            "longitude": 20,
            "owner_id": self.user.id,
            "amenities": []
        })

    def test_create_review_valid(self):
        data = {"text": "Great stay!",
                "user_id": self.user.id, "place_id": self.place.id}
        review = self.facade.create_review(data)
        self.assertEqual(review.text, "Great stay!")
        self.assertIn(review, self.place.reviews)
        self.assertIn(review, self.user.reviews)

    def test_create_review_empty_text(self):
        data = {"text": "", "user_id": self.user.id, "place_id": self.place.id}
        with self.assertRaises(ValueError):
            self.facade.create_review(data)

    def test_create_review_invalid_user(self):
        data = {"text": "Nice", "user_id":
                "wrong-id", "place_id": self.place.id}
        with self.assertRaises(ValueError):
            self.facade.create_review(data)

    def test_create_review_invalid_place(self):
        data = {"text": "Nice", "user_id":
                self.user.id, "place_id": "wrong-id"}
        with self.assertRaises(ValueError):
            self.facade.create_review(data)


if __name__ == "__main__":
    unittest.main()
