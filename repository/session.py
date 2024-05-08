from abc import ABC, abstractmethod
from typing import Union

from models import data

class Session(ABC): 
  @abstractmethod
  def create(self, user_id: int, code: str) -> Union[int, None]:
    pass
  
  @abstractmethod
  def get_user_settings(self, session_id: int) -> Union[data.User, None]:
    pass

  @abstractmethod
  def get_id_by_code(self, session_code: str) -> Union[int, None]:
    pass
    