from typing import Dict, Union

import models.data as data
import repository

class Session(repository.Session):
  __codes: Dict[str, int]
  __ids: Dict[int, int]
  __current_id: int

  __user: repository.User

  def __init__(self, user: repository.User):
    self.__codes = {}
    self.__ids = {}
    self.__current_id = 0

    self.__user = user

  def create(self, user_id: int, code: str) -> Union[int, None]:
    self.__current_id += 1

    self.__codes[code] = user_id
    self.__ids[self.__current_id] = user_id

    return self.__current_id
  
  def get_user_settings(self, session_id: int) -> Union[data.User, None]:
    if session_id in self.__ids:
      user_id = self.__ids[session_id]

      return self.__user.get_user_settings(user_id)

    return None
    