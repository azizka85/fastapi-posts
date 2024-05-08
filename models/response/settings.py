from pydantic import BaseModel

from constants import SETTINGS_POSTS_PER_PAGE, SETTINGS_DISPLAY_EMAIL

from models import data

class Settings(BaseModel):
  posts_per_page: int = SETTINGS_POSTS_PER_PAGE
  display_email: bool = SETTINGS_DISPLAY_EMAIL

  def from_data(self, settings: data.Settings):
    self.posts_per_page = settings.posts_per_page
    self.display_email = settings.display_email
