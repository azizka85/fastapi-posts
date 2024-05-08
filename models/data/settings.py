from constants import SETTINGS_POSTS_PER_PAGE, SETTINGS_DISPLAY_EMAIL

class Settings:
  id: int
  user_id: int
  posts_per_page: int
  display_email: bool

  def __init__(self, user_id: int):
    self.id = 0
    self.user_id = user_id
    self.posts_per_page = SETTINGS_POSTS_PER_PAGE
    self.display_email = SETTINGS_DISPLAY_EMAIL
