from typing import Union

from models.data.settings import Settings

class User:
  id: int
  first_name: str
  last_name: str
  email: Union[str, None]
  password: Union[str, None]

  settings: Settings

  def __init__(self, first_name: str, last_name: str, email: Union[str, None], password: Union[str, None]):
    self.id = 0
    self.first_name = first_name
    self.last_name =last_name
    self.email = email
    self.password = password

    self.settings = Settings(self.id)
