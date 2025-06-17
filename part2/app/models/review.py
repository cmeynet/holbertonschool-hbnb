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
    def __init__(self, id, text, rating, place, user):
        """
        Initialize Review with validation delegated to setters
        """
        super()._init__()

        self.id = id
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        


