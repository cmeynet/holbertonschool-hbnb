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

    def test_add_and_remove_place(self):
        p = Place("Maison", 120.0, 48.0, 2.0, self.user)
        self.user.add_place(p)
        self.assertIn(p, self.user.places)
        self.user.remove_place(p)
        self.assertNotIn(p, self.user.places)

    def test_admin_user(self):
        admin = User("Admin", "User", "admin@example.com", is_admin=True)
        self.assertTrue(admin.is_admin)

    def test_remove_nonexistent_place(self):
        p = Place("Maison", 120.0, 48.0, 2.0, self.user)
        # Pas ajouté à la liste, mais on tente de le retirer !
        self.user.remove_place(p)
        self.assertNotIn(p, self.user.places)


if __name__ == "__main__":
    unittest.main()
