from .baseclass import BaseModel
from .place import Place
from .user import User
from app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
	__tablename__ = "reviews"
	
	text = db.Column(db.Text, nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
	user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

	
	@validates('text')
	def validate_text(self, key, value):
		if not value:
			raise ValueError("Text cannot be empty")
		if not isinstance(value, str):
			raise TypeError("Text must be a string")
		return value

	@validates('rating')
	def validate_rating(self, key, value):
		if not isinstance(value, int):
			raise TypeError("Rating must be an integer")
		super().is_between('Rating', value, 0, 6)
		return value

	"""@property
	def place(self):
		return self.__place
	
	@place.setter
	def place(self, value):
		if not isinstance(value, Place):
			raise TypeError("Place must be a place instance")
		self.__place = value

	@property
	def user(self):
		return self.__user
	
	@user.setter
	def user(self, value):
		if not isinstance(value, User):
			raise TypeError("User must be a user instance")
		self.__user = value"""

	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'rating': self.rating,
			'place_id': self.place.id,
			'user_id': self.user.id
		}
