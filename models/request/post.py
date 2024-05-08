from pydantic import BaseModel

from models import data

class Post(BaseModel):
  title: str
  text: str = ''
  abstract: str = ''

  def to_data(self) -> data.Post:
    return data.Post(
      self.title,
      self.text,
      self.abstract,
      False,
      None
    )
