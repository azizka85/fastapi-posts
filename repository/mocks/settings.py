from typing import Dict, Union

from models import data
import repository

class Settings(repository.Settings):
  __settings: Dict[int, data.Settings]
  __user_ids: Dict[int, int]
  __current_id: int

  def __init__(self):
    self.__settings = {}
    self.__user_ids = {}
    self.__current_id = 0

  def create(self, settings: data.Settings) -> Union[int, None]:
    settings_id = None

    if settings.user_id in self.__user_ids:
      settings_id = self.__user_ids[settings.user_id]
    else:
      self.__current_id += 1
      settings_id = self.__current_id

    if settings_id:
      settings.id = settings_id

      self.__settings[settings_id] = settings
      self.__user_ids[settings.user_id] = settings_id

    return settings_id
  
  def edit(self, settings: data.Settings) -> bool:
    if settings.user_id not in self.__user_ids:
      return False

    settings_id = self.__user_ids[settings.user_id]

    settings.id = settings_id

    current = self.__settings[settings_id]

    current.display_email = settings.display_email
    current.posts_per_page = settings.posts_per_page

    return True
