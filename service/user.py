from typing import Union
from uuid import uuid1

from models import request
from models import response

import repository

class User:
  __user_repository: repository.User
  __session_repository: repository.Session

  def __init__(
    self, user_repository: repository.User, 
    session_repository: repository.Session
  ):
    self.__user_repository = user_repository
    self.__session_repository = session_repository

  def get_from_session(self, session_id: Union[int, None], session_code: str) -> Union[response.User, None]:
    if not session_id:
      return None
    
    user = self.__session_repository.get_user_settings(session_id)
    
    if not user:
      return None
    
    res = response.User()
    res.from_data(user, session_code)

    return res

  def get_from_session_code(self, session_code: str) -> Union[response.User, None]:
    session_id = self.__session_repository.get_id_by_code(session_code)

    return self.get_from_session(session_id, session_code)

  def get(self, user_id: Union[int, None]) -> Union[response.User, None]:
    if not user_id:
      return None

    session_code = str(uuid1())
    session_id = self.__session_repository.create(user_id, session_code)
    
    return self.get_from_session(session_id, session_code)

  def login(self, email: str, pwd: str) -> Union[response.User, None]:
    user_id = self.__user_repository.get_id(email, pwd)

    return self.get(user_id)
  
  def register(self, user: request.User) -> Union[response.User, None]:
    user_data = user.to_data()

    user_id = self.__user_repository.create(user_data)

    return self.get(user_id)
  
  def edit_settings(self, user: Union[response.User, None], settings: request.Settings) -> bool:
    if not user:
      return False
      
    settings_data = settings.to_data(user.id)
    
    return self.__user_repository.edit(settings_data)    
