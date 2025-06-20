# Add the “part2/” folder to the import path so that “app”
# is recognized as a module, otherwise it generates 1 error!
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

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
            Amenity("x" * 51)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Amenity("")

if __name__ == "__main__":
    unittest.main()
import unittest
