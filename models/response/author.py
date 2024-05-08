from typing import Union
from pydantic import BaseModel

from models import data

class Author(BaseModel):
  first_name: str = ''
  last_name: str = ''
  email: Union[str, None] = None

  def from_data(self, user: data.User):
    self.first_name = user.first_name
    self.last_name = user.last_name

    if user.settings.display_email:
      self.email = user.email

