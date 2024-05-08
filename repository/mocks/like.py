from typing import Dict, Set

import repository

class Like(repository.Like):
  __likes: Dict[int, Set[int]]

  def __init__(self):
    self.__likes = {}

  def create(self, user_id: int, post_id: int):
    if user_id not in self.__likes:
      self.__likes[user_id] = set()

    self.__likes[user_id].add(post_id)

  def delete(self, user_id: int, post_id: int):
    if user_id in self.__likes:
      self.__likes[user_id].remove(post_id)

  def get_post_ids(self, user_id: int) -> Set[int]:
    if user_id in self.__likes:
      return self.__likes[user_id]
    
    return set()
