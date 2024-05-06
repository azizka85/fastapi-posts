from abc import ABC, abstractmethod
from typing import Union

import models.data as data

class Session(ABC): 
  @abstractmethod
  def create(self, user_id: int, code: str) -> Union[int, None]:
    pass
  
  @abstractmethod
  def get_user_settings(self, session_id: int) -> Union[data.User, None]:
    pass
    