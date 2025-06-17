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

        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first name")
        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last name")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email")

        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__is_admin = is_admin

    @property
    def first_name(self):
        """
        Getter for first name
        """
        return self.__first_name

    @property
    def last_name(self):
        """
        Getter for last name
        """
        return self.__last_name

    @property
    def email(self):
        """
        Getter for email
        """
        return self.__email

    @property
    def is_admin(self):
        """
        Getter for admin status
        """
        return self.__is_admin


    @first_name.setter
    def first_name(self, value):
        """
        Setter for first name with validation
        """
        if not value or len(value) > 50:
            raise ValueError("Invalid first name")
        self.__first_name = value
        self.save()

    @last_name.setter
    def last_name(self, value):
        """
        Setter for last name with validation
        """
        if not value or len(value) > 50:
            raise ValueError("Invalid last name")
        self.__last_name = value
        self.save()

    @email.setter
    def email(self, new_email):
        """
        Setter for email with validation
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            raise ValueError("Invalid email format")
        self.__email = new_email
        self.save()

    @is_admin.setter
    def is_admin(self, value):
        """
        Setter for admin status with boolean check
        """
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self.__is_admin = value
        self.save()
