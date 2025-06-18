import unittest
from app.models.amenity import Amenity

class TestAmenityModel(unittest.TestCase):

    def test_valid_amenity(self):
        a = Amenity("Jacuzzi")
        self.assertEqual(a.name, "Jacuzzi")

    def test_invalid_name_type(self):
        with self.assertRaises(TypeError):
            Amenity(123)

    def test_name_too_long(self):
        with self.assertRaises(ValueError):
            Amenity("x" * 100)

if __name__ == "__main__":
    unittest.main()
