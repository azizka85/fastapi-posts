from typing import Union

import repository

class Like:
  __like_repository: repository.Like

  def __init__(self, like_repository: repository.Like):
    self.__like_repository = like_repository

  def create(self, user_id: Union[int, None], post_id: int) -> bool:
    if not user_id:
      return False
    
    self.__like_repository.create(user_id, post_id)

    return True
  
  def delete(self, user_id: Union[int, None], post_id: int) -> bool:
    if not user_id:
      return False
    
    self.__like_repository.delete(user_id, post_id)

    return True
