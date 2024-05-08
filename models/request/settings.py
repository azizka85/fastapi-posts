from pydantic import BaseModel

from models import data

class Settings(BaseModel):
  posts_per_page: int
  display_email: bool

  def to_data(self, user_id: int) -> data.Settings:
    settings = data.Settings()

    settings.user_id = user_id
    settings.posts_per_page = self.posts_per_page
    settings.display_email = self.display_email

    return settings
