#!/usr/bin/python3
"""
Review model representing reviews for places
"""
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    """
    Review entity with validation and attributes
    """
    def __init__(self, text, rating, place, user):
        """
        Initialize Review with validation delegated to setters
        """
        super()._init__()

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
        self.save()



