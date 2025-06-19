# Add the “part2/” folder to the import path so that “app”
# is recognized as a module, otherwise it generates 1 error!
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
from app.models.user import User
from app.models.place import Place


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User("Elie", "Boutin", "elie.boutin@exemple.fr")

    def test_valid_user(self):
        self.assertEqual(self.user.first_name, "Elie")
        self.assertEqual(self.user.last_name, "Boutin")
        self.assertEqual(self.user.email, "elie.boutin@exemple.fr")
        self.assertFalse(self.user.is_admin)

    def test_admin_user(self):
        admin = User("Admin", "User", "admin@example.com", is_admin=True)
        self.assertTrue(admin.is_admin)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Elie", "Boutin", "invalid-email")

    def test_invalid_first_name(self):
        with self.assertRaises(ValueError):
            User("", "Boutin", "elie.boutin@exemple.fr")

    def test_first_name_too_long(self):
        with self.assertRaises(ValueError):
            User("Victoire" * 51, "Boutin", "victoire@exemple.com")

    def test_invalid_last_name(self):
        with self.assertRaises(ValueError):
            User("Elie", "", "elie.boutin@exemple.fr")

    def test_last_name_too_long(self):
        with self.assertRaises(ValueError):
            User("Isabelle", "Rehri" * 51, "isabelle@exemple.com")

    def test_add_and_remove_place(self):
        p = Place("Maison", 120.0, 48.0, 2.0, self.user)
        self.user.add_place(p)
        self.assertIn(p, self.user.places)
        self.user.remove_place(p)
        self.assertNotIn(p, self.user.places)


if __name__ == "__main__":
    unittest.main()
