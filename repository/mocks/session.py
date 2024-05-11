from typing import Dict, Union

from models import data
import repository

class Session(repository.Session):
  __codes: Dict[str, int]
  __ids: Dict[int, int]
  __current_id: int

  __user_repository: repository.User

  def __init__(self, user_repository: repository.User):
    self.clear()

    self.__user_repository = user_repository

  def clear(self):
    self.__codes = {}
    self.__ids = {}
    self.__current_id = 0

  def create(self, user_id: int, code: str) -> Union[int, None]:
    self.__current_id += 1

    self.__codes[code] = self.__current_id
    self.__ids[self.__current_id] = user_id

    return self.__current_id
  
  def get_user_settings(self, session_id: int) -> Union[data.User, None]:
    if session_id in self.__ids:
      user_id = self.__ids[session_id]

      return self.__user_repository.get_user_settings(user_id)

    return None
    
  def get_id_by_code(self, session_code: str) -> Union[int, None]:
    if session_code in self.__codes:
      return self.__codes[session_code]
    
    return None
