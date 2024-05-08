from pydantic import BaseModel

from models import data

class User(BaseModel):
  first_name: str
  last_name: str
  email: str
  password: str

  def to_data(self) -> data.User:
    return data.User(
      self.first_name,
      self.last_name,
      self.email,
      self.password
    )        
