from typing import Dict, Union
import copy

from models import data
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
    self.__current_id += 1
    token = f'{user.email}-{user.password}'
    
    self.__tokens[token] = self.__current_id
    self.__users[self.__current_id] = user

    user.id = self.__current_id
    user.settings.user_id = self.__current_id            

    return self.__current_id

  def get_id(self, email: str, pwd: str) -> Union[int, None]:
    token = f'{email}-{pwd}'

    if token in self.__tokens:
      return self.__tokens[token]
    
    return None
  
  def get_user_settings(self, id: int) -> Union[data.User, None]:
    user = None

    if id in self.__users:
      user = copy.copy(self.__users[id])

      if not user.settings.display_email:
        user.email = None      
    
    return user

  def edit(self, settings: data.Settings) -> bool:
    if settings.user_id not in self.__users:
      return False    

    current = self.__users[settings.user_id]

    current.settings.display_email = settings.display_email
    current.settings.posts_per_page = settings.posts_per_page

    return True
