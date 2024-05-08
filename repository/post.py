from abc import ABC, abstractmethod
from typing import Union, List

from models import data

class Post(ABC):
  @abstractmethod
  def create(self, user_id: Union[int, None], post: data.Post) -> Union[int, None]:
    pass

  @abstractmethod
  def get(self, id: int, user_id: Union[int, None]) -> Union[data.Post, None]:
    pass

  @abstractmethod
  def list(self, user_id: Union[int, None]) -> List[data.Post]:
    pass

  @abstractmethod
  def liked_list(self, user_id: Union[int, None]) -> List[data.Post]:
    pass
