from typing import Dict, Union

import models.data as data
import repository

class User(repository.User):
  __users: Dict[int, data.User]
  __tokens: Dict[str, int]
  __current_id: int

  def __init__(self) -> None:
    self.__users = {}
    self.__tokens = {}
    self.__current_id = 0

  def create(self, user: data.User) -> Union[int, None]:
    token = f'{user.email}-{user.password}'
    user_id = None

    if token in self.__tokens:
      user_id = self.__tokens[token]
    else:
      self.__current_id += 1
      user_id = self.__current_id

    if user_id:
      user.id = user_id
      user.settings.user_id = user_id
      
      self.__users[user_id] = user
      self.__tokens[token] = user_id

    return user_id

  def get_id(self, email: str, pwd: str) -> Union[int, None]:
    token = f'{email}-{pwd}'

    if token in self.__tokens:
      return self.__tokens[token]
    
    return None
  
  def get_user_settings(self, id: int) -> Union[data.User, None]:
    if id in self.__users:
      return self.__users[id]
    
    return None
