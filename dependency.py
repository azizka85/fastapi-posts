from typing import Annotated

from fastapi import Depends

import service
import repository.postgresql
import repository.mocks

user_test_repository = repository.mocks.User()
session_test_repository = repository.mocks.Session(user_test_repository)
like_test_repository = repository.mocks.Like()
post_test_repository = repository.mocks.Post(like_test_repository, user_test_repository)

def clear_test_data():
  post_test_repository.clear()
  like_test_repository.clear()
  session_test_repository.clear()
  user_test_repository.clear()

user_test_service = service.User(user_test_repository, session_test_repository)
post_test_service = service.Post(post_test_repository)
like_test_service = service.Like(like_test_repository)

user_repository = repository.postgresql.User()
session_repository = repository.postgresql.Session(user_repository)
like_repository = repository.postgresql.Like()
post_repository = repository.postgresql.Post()

user_service = service.User(user_repository, session_repository)
post_service = service.Post(post_repository)
like_service = service.Like(like_repository)

def get_user_service(test: bool = False) -> service.User:
  if not test:
    return user_service
  
  return user_test_service

UserServiceDependency = Annotated[service.User, Depends(get_user_service)]

def get_post_service(test: bool = False) -> service.Post:
  if not test:
    return post_service
  
  return post_test_service

PostServiceDependency = Annotated[service.Post, Depends(get_post_service)]

def get_like_service(test: bool = False) -> service.Like:
  if not test:
    return like_service
  
  return like_test_service

LikeServiceDependency = Annotated[service.Like, Depends(get_like_service)]
