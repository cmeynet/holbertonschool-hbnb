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


