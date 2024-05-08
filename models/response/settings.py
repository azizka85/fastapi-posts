from pydantic import BaseModel

from models import data

class Settings(BaseModel):
  posts_per_page: int = 10
  display_email: bool = False

  def from_data(self, settings: data.Settings):
    self.posts_per_page = settings.posts_per_page
    self.display_email = settings.display_email
