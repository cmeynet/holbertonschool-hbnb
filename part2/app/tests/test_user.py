# Ajoute le dossier "part2/" au chemin d'import pour que "app"
# soit reconnu comme module sinon ça génère 1 erreur !
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

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("Elie", "Boutin", "invalid-email")

    def test_invalid_first_name(self):
        with self.assertRaises(ValueError):
            User("", "Boutin", "elie.boutin@exemple.fr")

    def test_invalid_last_name(self):
        with self.assertRaises(ValueError):
            User("Elie", "", "elie.boutin@exemple.fr")

    def test_add_and_remove_place(self):
        p = Place("Maison", 120.0, 48.0, 2.0, self.user)
        self.user.add_place(p)
        self.assertIn(p, self.user.places)
        self.user.remove_place(p)
        self.assertNotIn(p, self.user.places)


if __name__ == "__main__":
    unittest.main()
