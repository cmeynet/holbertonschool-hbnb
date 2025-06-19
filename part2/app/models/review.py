#!/usr/bin/python3
"""
Review model representing reviews for places
"""
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    _storage = {}  # stockage en mémoire simulé
    """
    Review entity with validation and attributes
    """
    def __init__(self, text, rating, place, user):
        """
        Initialize Review with validation delegated to setters
        """
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """
        Getter for review text !
        """
        return self.__text

    @text.setter
    def text(self, value):
        """
        Setter for review text with basic validation
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string")
        self.__text = value

    @property
    def rating(self):
        """
        Getter for review rating
        """
        return self.__rating

    @rating.setter
    def rating(self, value):
        """
        Setter for review rating with range validation
        """
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value

    @property
    def place(self):
        """
        Getter for reviewed Place
        """
        return self.__place

    @place.setter
    def place(self, value):
        """
        Setter for place with instance type check
        """
        if not isinstance(value, Place):
            raise TypeError("place must be a Place instance")
        self.__place = value

    @property
    def user(self):
        """
        Getter for review author (User)
        """
        return self.__user

    @user.setter
    def user(self, value):
        """
        Setter for user with instance type check
        """
        if not isinstance(value, User):
            raise TypeError("user must be a User instance")
        self.__user = value

    def to_dict(self):
        """
        Convert the Review instance to a dictionary
        """
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id if self.place else None,
            "user_id": self.user.id if self.user else None,
            # "created_at": self.created_at.isoformat(),
            # "updated_at": self.updated_at.isoformat()
        }
