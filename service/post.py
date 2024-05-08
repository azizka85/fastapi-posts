from typing import List, Union

from models import data
from models import response
from models import request
import repository

class Post:
  __post_repository: repository.Post

  def __init__(self, post_repository: repository.Post):
    self.__post_repository = post_repository

  def list(self, user_id: Union[int, None]) -> List[response.Post]:
    return response.Post.from_list(
      self.__post_repository.list(user_id)
    )

  def liked_list(self, user_id: Union[int, None]) -> List[response.Post]:
    return response.Post.from_list(
      self.__post_repository.liked_list(user_id)
    )

  def get(self, id: int, user_id: Union[int, None]) -> Union[response.Post, None]:
    post = self.__post_repository.get(id, user_id)

    if not post:
      return None
    
    res = response.Post()
    res.from_data(post)

    return res

  def create(self, user_id: Union[int, None], post: request.Post) -> Union[int, None]:
    post_data = post.to_data()
    
    return self.__post_repository.create(user_id, post_data)
