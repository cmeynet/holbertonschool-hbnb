from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.extensions import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # USER
    def create_user(self, user_data):
        if self.user_repo.count() == 0:
            user_data['is_admin'] = True
        else:
            user_data['is_admin'] = user_data.get('is_admin', False)

        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user
    
    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    
    def update_user(self, current_user_id, user_id, user_data, is_admin=False):
        """
        Only the logged-in user can modify his profile.
        Sensitive fields (email, password) are protected.
        """
        if not is_admin and current_user_id != user_id:
            raise PermissionError("Unauthorized action")

        # FIX : protection champs email/password
        forbidden_fields = {"email", "password"}
        if not is_admin and forbidden_fields.intersection(user_data):
            raise ValueError("You cannot modify email or password")

        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    # PLACE
    def create_place(self, current_user_id, place_data):
        """POST /places/ : le propriétaire est forcé à current_user_id."""
        user = self.get_user(current_user_id)
        if not user:
            raise KeyError("User not found")

        # owner_id from the client is completely ignored
        place_data.pop("owner_id", None)

        amenities_payload = place_data.pop("amenities", None)

        place = Place(owner=user, **place_data)
        self.place_repo.add(place)
        user.add_place(place)

        # connects existing amenities
        if amenities_payload:
            for item in amenities_payload:
                amenity = self.get_amenity(item["id"])
                if not amenity:
                    raise KeyError("Invalid amenity id")
                place.add_amenity(amenity)
        
        db.session.commit()
        
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, current_user_id, place_id, place_data, is_admin=False):
        """
        Only owner can modifiate + if is_admin=True.
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")

        # Property control (skip if admin)
        if not is_admin and str(place.owner.id) != str(current_user_id):
            raise PermissionError("Unauthorized action")

        # Protected fields
        for k in ("owner", "owner_id", "id"):
            place_data.pop(k, None)

        # Convert amenity IDs to Amenity objects
        if "amenities" in place_data:
            amenity_ids = place_data.pop("amenities")
            new_amenities = []
            for aid in amenity_ids:
                amenity = self.get_amenity(aid)
                if not amenity:
                    raise KeyError(f"Amenity not found: {aid}")
                new_amenities.append(amenity)
                
            place.amenities = new_amenities

        self.place_repo.update(place_id, place_data)
        return place

    # REVIEWS
    def create_review(self, current_user_id, review_data):
        user = self.get_user(current_user_id)
        if not user:
            raise KeyError("User not found")

        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise KeyError("Place not found")

        if place.owner.id == current_user_id:
            raise ValueError("You cannot review your own place")
        
        if self.user_already_reviewed(current_user_id, place.id):
            raise ValueError("You have already reviewed this place")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            place_id=place.id,
            user_id=user.id
        )
        
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")
        return place.reviews

    def update_review(self, current_user_id, review_id, review_data, is_admin=False):
        """
        Update a review : only author can modifiate + if is an administrator
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise KeyError("Review not found")

        if not is_admin and str(review.user.id) != str(current_user_id):
            raise PermissionError("Unauthorized action")

        # For not change user and place
        review_data.pop("user_id", None)
        review_data.pop("place_id", None)

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, current_user_id, review_id, is_admin=False):
        """
        Delete a review : only author can delete + administrator
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise KeyError("Review not found")

        if not is_admin and str(review.user.id) != str(current_user_id):
            raise PermissionError("Unauthorized action")

        with db.session.no_autoflush:
            user = review.user
            place = review.place

            if review in user.reviews:
                user.reviews.remove(review)
            if review in place.reviews:
                place.reviews.remove(review)
            
            db.session.delete(review)
        db.session.commit()

    def user_already_reviewed(self, user_id: str, place_id: str) -> bool:
        """
        Return True if user user has already left a review on this place
        """
        return any(
            r.user.id == user_id and r.place.id == place_id
            for r in self.review_repo.get_all()
            )

