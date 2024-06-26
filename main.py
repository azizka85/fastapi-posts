import os
from dotenv import load_dotenv
from typing import Annotated, Union, List

from fastapi import Body, Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

import models.response as response
import models.request as request

import dependency

load_dotenv()

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    os.getenv('FRONTEND_HOST') # type: ignore
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.get('/test/clear')
def clear_test_data():
  dependency.clear_test_data()

@app.get('/user')
def get_user_by_session_code(
  user_service: dependency.UserServiceDependency,
  session_code: Annotated[Union[str, None], Header()] = None,  
) -> Union[response.User, None]:
  if not session_code:
    return None
  
  return user_service.get_from_session_code(session_code)

UserBySessionCodeDependency = Annotated[Union[response.User, None], Depends(get_user_by_session_code)]


@app.post('/sign-in')
def login(
  email: Annotated[str, Body()], password: Annotated[str, Body()],
  user_service: dependency.UserServiceDependency
) -> Union[response.User, None]:
  return user_service.login(email, password)

@app.post('/sign-up')
def register(
  user: request.User,
  user_service: dependency.UserServiceDependency
) -> Union[response.User, None]:
  return user_service.register(user)

@app.post("/settings/edit")
def edit_settings(
  user: UserBySessionCodeDependency,
  user_service: dependency.UserServiceDependency,
  settings: request.Settings
) -> bool:
  return user_service.edit_settings(user, settings)

@app.get("/")
def posts_list(
  user: UserBySessionCodeDependency,
  post_service: dependency.PostServiceDependency
) -> List[response.Post]:
  user_id = None

  if user:
    user_id = user.id

  return post_service.list(user_id)

@app.get("/liked")
def liked_posts_list(
  user: UserBySessionCodeDependency,
  post_service: dependency.PostServiceDependency
) -> List[response.Post]:
  user_id = None

  if user:
    user_id = user.id

  return post_service.liked_list(user_id)

@app.get("/{id}")
def post_get(
  user: UserBySessionCodeDependency,
  post_service: dependency.PostServiceDependency,
  id: int
) -> Union[response.Post, None]:
  user_id = None

  if user:
    user_id = user.id

  return post_service.get(id, user_id)

@app.post("/post/create")
def post_create(
  user: UserBySessionCodeDependency,
  post_service: dependency.PostServiceDependency,
  post: request.Post
) -> Union[int, None]:
  user_id = None

  if user:
    user_id = user.id

  return post_service.create(user_id, post)

@app.post("/like/create")
def like_create(
  user: UserBySessionCodeDependency,
  like_service: dependency.LikeServiceDependency,
  post_id: Annotated[int, Body()]
) -> bool:
  user_id = None

  if user:
    user_id = user.id

  return like_service.create(user_id, post_id)

@app.post("/like/delete")
def like_delete(
  user: UserBySessionCodeDependency,
  like_service: dependency.LikeServiceDependency,
  post_id: Annotated[int, Body()]
) -> bool:
  user_id = None

  if user:
    user_id = user.id

  return like_service.delete(user_id, post_id)
