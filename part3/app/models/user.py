from .baseclass import BaseModel
import re
from app.extensions import db, bcrypt
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = "users"
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    
    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value.strip():
            raise ValueError("First name must not be empty")
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length('First name', value, 50)
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value.strip():
            raise ValueError("Last name must not be empty")
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length('Last name', value, 50)
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    @validates('password')
    def validate_password(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        if not value.strip():
            raise ValueError("Password must not be empty")
        return self.hash_password(value)

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        return value


    def add_place(self, place):
        """
        Add a place
        """
        self.places.append(place)

    def add_review(self, review):
        """
        Add a new review
        """
        self.reviews.append(review)

    def delete_review(self, review):
        """
        Delete a review
        """
        self.reviews.remove(review)

    def hash_password(self, password):
        """
        Hashes the password before storing it.
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verifies if the provided password matches the hashed password.
        """
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
            # password not include for security reasons
        }
