from pydantic import BaseModel

from models import data

class User(BaseModel):
  first_name: str
  last_name: str
  email: str
  password: str

  def to_data(self) -> data.User:
    user = data.User()

    user.first_name = self.first_name
    user.last_name = self.last_name
    user.email = self.email
    user.password = self.password

    return user
