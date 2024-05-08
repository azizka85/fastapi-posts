from typing import Annotated

from fastapi import Depends

import service
import repository.mocks

settings_repository = repository.mocks.Settings()
user_repository = repository.mocks.User(settings_repository)
session_repository = repository.mocks.Session(user_repository)
like_repository = repository.mocks.Like()
post_repository = repository.mocks.Post(like_repository, user_repository)

user_service = service.User(user_repository, session_repository, settings_repository)
post_service = service.Post(post_repository)
like_service = service.Like(like_repository)

def get_user_service() -> service.User:
  return user_service

UserServiceDependency = Annotated[service.User, Depends(get_user_service)]

def get_post_service() -> service.Post:
  return post_service

PostServiceDependency = Annotated[service.Post, Depends(get_post_service)]

def get_like_service() -> service.Like:
  return like_service

LikeServiceDependency = Annotated[service.Like, Depends(get_like_service)]
