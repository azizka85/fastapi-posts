from typing import Union

from models.data.user import User

class Post:
  id: int
  title: str
  text: str
  abstract: str
  liked: bool

  author: Union[User, None]

  def __init__(self, title: str, text: str, abstract: str, liked: bool, author: Union[User, None]):
    self.id = 0
    self.title = title
    self.text = text
    self.abstract = abstract
    self.liked = liked
    
    self.author = author
