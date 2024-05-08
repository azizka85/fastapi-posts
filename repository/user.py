from abc import ABC, abstractmethod
from typing import Union

from models import data

class User(ABC):
  @abstractmethod
  def create(self, user: data.User) -> Union[int, None]:
    pass

  @abstractmethod  
  def get_id(self, email: str, pwd: str) -> Union[int, None]:
    pass

  @abstractmethod
  def get_user_settings(self, id: int) -> Union[data.User, None]:
    pass
