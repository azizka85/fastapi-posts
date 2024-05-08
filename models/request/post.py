from pydantic import BaseModel

from models import data

class Post(BaseModel):
  title: str
  text: str = ''
  abstract: str = ''

  def to_data(self) -> data.Post:
    post = data.Post()

    post.title = self.title
    post.text = self.text
    post.abstract = self.abstract

    return post
