from typing import Dict, List, Union

from models import data
import repository
from repository.mocks.like import Like
from repository.mocks.user import User

class Post(repository.Post):
  __posts: Dict[int, data.Post]
  __authors: Dict[int, Union[int, None]]
  __current_id: int

  __like_repository: Like
  __user_repository: User

  def __init__(self, like_repository: Like, user_repository: User):
    self.clear()

    self.__like_repository = like_repository
    self.__user_repository = user_repository

  def clear(self):
    self.__posts = {}
    self.__authors = {}
    self.__current_id = 0

  def create(self, user_id: Union[int, None], post: data.Post) -> Union[int, None]:
    self.__current_id += 1

    post.id = self.__current_id    
    
    self.__posts[self.__current_id] = post
    self.__authors[self.__current_id] = user_id

    return post.id

  def get(self, id: int, user_id: Union[int, None]) -> Union[data.Post, None]:
    liked = set()

    if user_id:
      liked = self.__like_repository.get_post_ids(user_id)

    if id in self.__posts:
      post = self.__posts[id]

      author_id = self.__authors[id]

      if author_id:
        post.author = self.__user_repository.get_user_settings(author_id)

      if id in liked:
        post.liked = True
      else:
        post.liked = False

      return post
    
    return None
  
  def list(self, user_id: Union[int, None]) -> List[data.Post]:
    liked = set()

    if user_id:
      liked = self.__like_repository.get_post_ids(user_id)
    
    posts = []

    for id, post in self.__posts.items():
      author_id = self.__authors[id]

      if author_id:
        post.author = self.__user_repository.get_user_settings(author_id)

      if id in liked:
        post.liked = True
      else:
        post.liked = False

      posts.append(post)

    return posts
  
  def liked_list(self, user_id: Union[int, None]) -> List[data.Post]:
    liked = set()

    if user_id:
      liked = self.__like_repository.get_post_ids(user_id)
    
    posts = []

    for id, post in self.__posts.items():
      if id in liked:
        author_id = self.__authors[id]

        if author_id:
          post.author = self.__user_repository.get_user_settings(author_id)

        post.liked = True
        posts.append(post)

    return posts
