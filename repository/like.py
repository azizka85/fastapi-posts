from abc import ABC, abstractmethod

class Like(ABC):
  @abstractmethod
  def create(self, user_id: int, post_id: int):
    pass

  @abstractmethod
  def delete(self, user_id: int, post_id: int):
    pass
