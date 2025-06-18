import unittest
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        self.owner = User("Alice", "Smith", "alice@example.com")

    def test_valid_place(self):
        p = Place("Villa", 200.0, 45.0, 3.0, self.owner, "Belle villa")
        self.assertEqual(p.title, "Villa")
        self.assertEqual(p.price, 200.0)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place("Loft", 100.0, 200.0, 2.0, self.owner)

    def test_add_amenity(self):
        p = Place("Chalet", 180.0, 45.0, 1.0, self.owner)
        a = Amenity("Wi-Fi")
        p.add_amenity(a)
        self.assertIn(a, p.amenities)

    def test_owner_must_be_user(self):
        with self.assertRaises(TypeError):
            Place("Cabane", 90.0, 40.0, 2.0, "not_a_user")

if __name__ == "__main__":
    unittest.main()
