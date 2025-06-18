#!/usr/bin/python3
"""
User model representing application users with basic info and admin status
"""
from app.models.base_model import BaseModel
import re


class User(BaseModel):
    """
    User entity with validation and protected attributes
    """
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize User with validation on inputs
        """
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        """
        Getter for first name
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """
        Setter for first name with validation
        """
        if not value or len(value) > 50:
            raise ValueError("Invalid first name")
        self.__first_name = value

    @property
    def last_name(self):
        """
        Getter for last name
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """
        Setter for last name with validation
        """
        if not value or len(value) > 50:
            raise ValueError("Invalid last name")
        self.__last_name = value

    @property
    def email(self):
        """
        Getter for email
        """
        return self.__email

    @email.setter
    def email(self, new_email):
        """
        Setter for email with validation
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            raise ValueError("Invalid email format")
        self.__email = new_email

    @property
    def is_admin(self):
        """
        Getter for admin status
        """
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        """
        Setter for admin status with boolean check
        """
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self.__is_admin = value

    def add_place(self, place):
        """
        Add a place to the user
        """
        self.places.append(place)

    def remove_place(self, place):
        """
        Remove a place from the user
        """
        if place in self.places:
            self.places.remove(place)

    def add_review(self, review):
        """
        Add a review to the user
        """
        self.reviews.append(review)

    def remove_review(self, review):
        """
        Remove a review from the user
        """
        if review in self.reviews:
            self.reviews.remove(review)

    def to_dict(self):
        """
        Convert the User instance to a dictionary
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            }
