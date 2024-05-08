from models import data
from models.response.author import Author
from models.response.settings import Settings

class User(Author):
  id: int = 0  
  session_code: str = ''

  settings: Settings = Settings()

  def from_data(self, user: data.User, session_code: str):
    super().from_data(user)

    self.id = user.id
    self.session_code = session_code

    self.settings.from_data(user.settings)
