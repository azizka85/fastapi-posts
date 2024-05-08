from abc import ABC, abstractmethod
from typing import Union

from models import data

class Settings(ABC):
  @abstractmethod
  def create(self, settings: data.Settings) -> Union[int, None]:
    pass

  @abstractmethod
  def edit(self, settings: data.Settings) -> bool:
    pass
