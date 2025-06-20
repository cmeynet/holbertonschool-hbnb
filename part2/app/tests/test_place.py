# Add the “part2/” folder to the import path so that “app”
# is recognized as a module, otherwise it generates 1 error!
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import unittest
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        self.owner = User("Anna", "Onen", "anna@exemple.fr")

    def test_valid_place(self):
        p = Place("Villa", 200.0, 45.0, 3.0, self.owner, "Belle villa")
        self.assertEqual(p.title, "Villa")
        self.assertEqual(p.price, 200.0)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            Place("Cabane", -10.0, 45.0, 1.0, self.owner)

    def test_price_type_float(self):
        with self.assertRaises(TypeError):
            Place("Maison", "100", 45.0, 1.0, self.owner)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place("Loft", 100.0, 200.0, 2.0, self.owner)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Place("Studio", 100.0, 40.0, 200.0, self.owner)

    def test_title_too_long(self):
        long_title = "Villa Mialane" * 101
        with self.assertRaises(ValueError):
            Place(long_title, 120.0, 45.0, 2.0, self.owner)
  
    def test_add_and_remove_amenity(self):
        p = Place("Cabane", 90.0, 45.0, 1.0, self.owner)
        a = Amenity("Jacuzzi")
        p.add_amenity(a)
        self.assertIn(a, p.amenities)
        p.delete_amenity(a)
        self.assertNotIn(a, p.amenities)

    def test_owner_must_be_user(self):
        with self.assertRaises(TypeError):
            Place("Duplex", 90.0, 40.0, 2.0, "not_a_user")

if __name__ == "__main__":
    unittest.main()
