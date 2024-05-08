from typing import Union, List
from pydantic import BaseModel

from models import data
from models.response.author import Author

class Post(BaseModel):
  id: int = 0
  title: str = ''
  text: str = ''
  abstract: str = ''
  liked: bool = False

  author: Union[Author, None] = None

  def from_data(self, post: data.Post):
    self.id = post.id
    self.title = post.title
    self.text = post.text
    self.abstract = post.abstract
    self.liked = post.liked

    if post.author:
      self.author = Author()
      self.author.from_data(post.author)

  @classmethod
  def from_list(cls, list: List[data.Post]) -> List['Post']:
    res = []

    for item in list:
      post = Post()
      post.from_data(item)
      res.append(post)

    return res
