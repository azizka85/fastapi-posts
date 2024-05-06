from dotenv import load_dotenv
from typing import Annotated, Union
from fastapi import FastAPI, Header, Depends

load_dotenv()

app = FastAPI()

def get_user(session_code: Annotated[Union[str, None], Header()] = None):
  if session_code == 'xyz-567':
    return 'User'
  else:
    return 'Anonym'

@app.get("/")
def posts_list(user: Annotated[str, Depends(get_user)]):
  return {"user": user}
