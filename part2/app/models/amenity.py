from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class to represent an amenity in the application."""

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        self.__name = value

    def to_dict(self):
        """Convert the Amenity instance to a dictionary representation."""
        return {
            "id": self.id,
            "name": self.name
        }
