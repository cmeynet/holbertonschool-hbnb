import unittest
import sys
import os

# Pour pouvoir importer app.models.user même en exécutant directement ce fichier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class TestUser(unittest.TestCase):

    def test_valid_user_creation(self):
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)
        self.assertEqual(user.places, [])
        self.assertEqual(user.reviews, [])

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Alice", "Lemoine", "notanemail")

    def test_empty_first_name(self):
        with self.assertRaises(ValueError):
            User("", "Lemoine", "alice@example.com")

    def test_long_last_name(self):
        with self.assertRaises(ValueError):
            User("Alice", "L" * 51, "alice@example.com")

    def test_is_admin_must_be_boolean(self):
        user = User("Alice", "Lemoine", "alice@example.com")
        with self.assertRaises(ValueError):
            user.is_admin = "yes"

    def test_add_place(self):
        user = User("Alice", "Lemoine", "alice@example.com")
        place = Place("Cabane", 80.0, 44.0, 3.0, user)
        user.add_place(place)
        self.assertIn(place, user.places)

    def test_remove_place(self):
        user = User("Alice", "Lemoine", "alice@example.com")
        place = Place("Cabane", 80.0, 44.0, 3.0, user)
        user.add_place(place)
        user.remove_place(place)
        self.assertNotIn(place, user.places)

    def test_add_review(self):
        user = User("Alice", "Lemoine", "alice@example.com")
        place = Place("Cabane", 80.0, 44.0, 3.0, user)
        review = Review("Super endroit", 5, place, user)
        user.add_review(review)
        self.assertIn(review, user.reviews)

    def test_remove_review(self):
        user = User("Alice", "Lemoine", "alice@example.com")
        place = Place("Cabane", 80.0, 44.0, 3.0, user)
        review = Review("Super endroit", 5, place, user)
        user.add_review(review)
        user.remove_review(review)
        self.assertNotIn(review, user.reviews)

    def test_to_dict(self):
        user = User("Alice", "Lemoine", "alice@example.com")
        result = user.to_dict()
        self.assertEqual(result["first_name"], "Alice")
        self.assertEqual(result["last_name"], "Lemoine")
        self.assertEqual(result["email"], "alice@example.com")
        self.assertIn("places", result)
        self.assertIn("reviews", result)

if __name__ == "__main__":
    unittest.main()
