from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repo.update(user_id, user_data)
        return user

    # Amenity
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
    
    # Place
    def create_place(self, place_data):
        # Charge the owner
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # Charge the amenities
        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity '{amenity_id}' not found")
            amenities.append(amenity)

        # Create the location with the `User` object, not just its ID
        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            amenities=amenities
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        self.place_repo.update(place_id, place_data)
        return place

    # Review
    def create_review(self, review_data):
        text = review_data.get('text')
        rating = review_data.get('rating')
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        review = Review(text, rating, place, user)

        self.review_repo.add(review)
        place.add_review(review)
        user.add_review(review)

        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)

        text = review_data.get('text')
        rating = review_data.get('rating')

        if text is not None:
            review.text = text

        if rating is not None:
            review.rating = rating

        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)

        review.place.delete_review(review)
        review.user.remove_review(review)

        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}
