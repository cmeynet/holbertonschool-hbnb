# Add the “part2/” folder to the import path so that “app”
# is recognized as a module, otherwise it generates 1 error!
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class TestReviewModel(unittest.TestCase):
    def setUp(self):
        self.user = User("Clemence", "Meynet", "clemence@exemple.com")
        self.place = Place("Studio", 100.0, 45.0, 1.0, self.user)

    def test_valid_review(self):
        r = Review("Lieu très agréable", 5, self.place, self.user)
        self.assertEqual(r.text, "Lieu très agréable")
        self.assertEqual(r.rating, 5)
        self.assertEqual(r.place, self.place)
        self.assertEqual(r.user, self.user)

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            Review("", 3, self.place, self.user)

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review("Top", 6, self.place, self.user)

    def test_user_must_be_user_instance(self):
        with self.assertRaises(TypeError):
            Review("Cool", 4, self.place, "not_a_user")

    def test_place_must_be_place_instance(self):
        with self.assertRaises(TypeError):
            Review("Cool", 4, "not_a_place", self.user)

if __name__ == "__main__":
    unittest.main()


