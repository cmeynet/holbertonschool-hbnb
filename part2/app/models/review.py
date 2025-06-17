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


