from typing import Union

from models.data.user import User

class Post:
  id = 0
  title = ''
  text = ''
  abstract = ''
  liked = False

  author: Union[User, None] = None
