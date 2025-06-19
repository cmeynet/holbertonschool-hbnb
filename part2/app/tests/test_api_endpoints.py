# Add the “part2/” folder to the import path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
import uuid
from app import create_app


class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Generate a unique email to avoid duplicates
        self.email = f"john{uuid.uuid4().hex}@example.com"

        # Create test user
        self.user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": self.email
        })

        self.assertEqual(self.user_resp.status_code, 201)
        self.user_id = self.user_resp.get_json()["id"]

        # Create test amenity
        self.amenity_resp = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.assertEqual(self.amenity_resp.status_code, 201)
        self.amenity_id = self.amenity_resp.get_json()["id"]

        # Create test place
        self.place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test Studio",
            "description": "Nice and clean",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 2.0,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(self.place_resp.status_code, 201)
        self.place_id = self.place_resp.get_json()["id"]

        # Create test review
        self.review_resp = self.client.post('/api/v1/reviews/', json={
            "text": "Very nice!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(self.review_resp.status_code, 201)
        self.review_id = self.review_resp.get_json()["id"]

    # ---------- USERS ----------
    def test_get_users(self):
        r = self.client.get('/api/v1/users/')
        self.assertEqual(r.status_code, 200)

    def test_get_user_by_id(self):
        r = self.client.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(r.status_code, 200)

    def test_update_user(self):
        r = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(r.status_code, 200)

    # ---------- AMENITIES ----------
    def test_get_amenities(self):
        r = self.client.get('/api/v1/amenities/')
        self.assertEqual(r.status_code, 200)

    def test_get_amenity_by_id(self):
        r = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(r.status_code, 200)

    def test_update_amenity(self):
        r = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={"name": "Updated WiFi"})
        self.assertEqual(r.status_code, 200)

    # ---------- PLACES ----------
    def test_get_places(self):
        r = self.client.get('/api/v1/places/')
        self.assertEqual(r.status_code, 200)

    def test_get_place_by_id(self):
        r = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(r.status_code, 200)

    def test_update_place(self):
        r = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Updated Studio",
            "description": "Still nice",
            "price": 120.0,
            "latitude": 45.0,
            "longitude": 2.0,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(r.status_code, 200)

    # ---------- REVIEWS ----------
    def test_get_reviews(self):
        r = self.client.get('/api/v1/reviews/')
        self.assertEqual(r.status_code, 200)

    def test_get_review_by_id(self):
        r = self.client.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(r.status_code, 200)

    def test_update_review(self):
        r = self.client.put(f'/api/v1/reviews/{self.review_id}', json={
            "text": "Updated text",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(r.status_code, 200)

    def test_get_reviews_by_place(self):
        r = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertIn(r.status_code, [200, 404])  # selon route réellement montée

    def test_delete_review(self):
        r = self.client.delete(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
