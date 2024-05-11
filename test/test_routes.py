import os
import sys

sys.path.append(os.getcwd())

import unittest
from fastapi.testclient import TestClient

import dependency

from constants import SETTINGS_POSTS_PER_PAGE, SETTINGS_DISPLAY_EMAIL

from main import app, request, response 

class TestRoutes(unittest.TestCase):
  __client: TestClient

  def setUp(self):
    self.__client = TestClient(app)    

  def test_user(self):
    dependency.clear_test_data()

    user = request.User(first_name='__test_1__', last_name='__test_1__', email='__test__@1.again', password='test')

    register_res = self.__client.post(
      '/sign-up?test=true', 
      json=vars(user)
    )

    register_data = response.User(**register_res.json())

    self.assertIsNotNone(register_data.id)
    self.assertEqual(register_data.first_name, user.first_name)
    self.assertEqual(register_data.last_name, user.last_name)
    if not SETTINGS_DISPLAY_EMAIL:
      self.assertIsNone(register_data.email)
    else:
      self.assertEqual(register_data.email, user.email)
    self.assertIsNotNone(register_data.session_code)

    self.assertEqual(register_data.settings.posts_per_page, SETTINGS_POSTS_PER_PAGE)
    self.assertEqual(register_data.settings.display_email, SETTINGS_DISPLAY_EMAIL)

    session_res = self.__client.get(
      '/user?test=true',
      headers={
        'session-code': register_data.session_code
      }
    )

    session_data = response.User(**session_res.json())

    self.assertEqual(session_data.id, register_data.id)
    self.assertEqual(session_data.first_name, register_data.first_name)
    self.assertEqual(session_data.last_name, register_data.last_name)
    if not SETTINGS_DISPLAY_EMAIL:
      self.assertIsNone(session_data.email)
    else:
      self.assertEqual(session_data.email, user.email)
    self.assertEqual(session_data.session_code, register_data.session_code)

    self.assertEqual(session_data.settings.posts_per_page, register_data.settings.posts_per_page)
    self.assertEqual(session_data.settings.display_email, register_data.settings.display_email)

    login_res = self.__client.post(
      '/sign-in?test=true',
      json={
        'email': user.email,
        'password': user.password
      }
    )

    login_data = response.User(**login_res.json())

    self.assertEqual(login_data.id, register_data.id)
    self.assertEqual(login_data.first_name, user.first_name)
    self.assertEqual(login_data.last_name, user.last_name)
    self.assertEqual(login_data.email, register_data.email)
    self.assertIsNotNone(login_data.session_code)

    self.assertEqual(login_data.settings.posts_per_page, SETTINGS_POSTS_PER_PAGE)
    self.assertEqual(login_data.settings.display_email, SETTINGS_DISPLAY_EMAIL)

    settings = request.Settings(
      posts_per_page=30,
      display_email=True
    )

    settings_res = self.__client.post(
      '/settings/edit?test=true',
      headers={
        'session-code': login_data.session_code
      },
      json=vars(settings)
    )

    self.assertEqual(settings_res.text, 'true')

    session_from_register_res = self.__client.get(
      '/user?test=true',
      headers={
        'session-code': register_data.session_code
      }
    )

    session_from_register_data = response.User(**session_from_register_res.json())

    self.assertEqual(session_from_register_data.email, user.email)
    self.assertEqual(session_from_register_data.settings.posts_per_page, settings.posts_per_page)
    self.assertEqual(session_from_register_data.settings.display_email, settings.display_email)

    session_from_login_res = self.__client.get(
      '/user?test=true',
      headers={
        'session-code': login_data.session_code
      }
    )

    session_from_login_data = response.User(**session_from_login_res.json())

    self.assertEqual(session_from_login_data.email, user.email)
    self.assertEqual(session_from_login_data.settings.posts_per_page, settings.posts_per_page)
    self.assertEqual(session_from_login_data.settings.display_email, settings.display_email)

  def test_post(self):
    dependency.clear_test_data()

    user = request.User(first_name='test2', last_name='test2', email='test@2.again', password='test')

    register_res = self.__client.post(
      '/sign-up?test=true', 
      json=vars(user)
    )

    register_data = response.User(**register_res.json())

    post = request.Post(title='title', text='text', abstract='abstract')

    create_post_res = self.__client.post(
      "/post/create?test=true",
      headers={
        'session-code': register_data.session_code
      },
      json=vars(post)
    )

    self.assertNotEqual(create_post_res.text, 'null')

    post_id = int(create_post_res.text)

    self.assertGreater(post_id, 0)

    posts_list_res = self.__client.get(
      '/?test=true',
      headers={
        'session-code': register_data.session_code
      }
    )

    posts_list_data = [response.Post(**d) for d in posts_list_res.json()]

    self.assertGreater(len(posts_list_data), 0)

    searched_posts = list(
      filter(lambda p: p.id == post_id, posts_list_data)
    )

    self.assertGreater(len(searched_posts), 0)

    for item in searched_posts:
      self.assertEqual(item.author.first_name, register_data.first_name) # type: ignore
      self.assertEqual(item.author.last_name, register_data.last_name) # type: ignore
      self.assertEqual(item.author.email, register_data.email) # type: ignore            

    post_res = self.__client.get(
      f'/{post_id}?test=true',
      headers={
        'session-code': register_data.session_code
      }
    )

    post_data = response.Post(**post_res.json())

    self.assertEqual(post_data.id, post_id)
    self.assertEqual(post_data.title, post.title)
    self.assertEqual(post_data.text, post.text)
    self.assertEqual(post_data.abstract, post.abstract)
    self.assertIs(post_data.liked, False)

    self.assertIsNotNone(post_data.author)
    self.assertEqual(post_data.author.first_name, register_data.first_name) # type: ignore
    self.assertEqual(post_data.author.last_name, register_data.last_name) # type: ignore
    self.assertEqual(post_data.author.email, register_data.email) # type: ignore

    liked_posts_res = self.__client.get(
      "/liked?test=true",
      headers={
        'session-code': register_data.session_code
      }
    )

    liked_posts_data = [response.Post(**d) for d in liked_posts_res.json()]

    self.assertEqual(len(liked_posts_data), 0)

    post_create_like_res = self.__client.post(
      '/like/create?test=true',
      headers={
        'session-code': register_data.session_code
      },
      json=post_id
    )

    self.assertEqual(post_create_like_res.text, 'true')

    liked_posts_res_2 = self.__client.get(
      "/liked?test=true",
      headers={
        'session-code': register_data.session_code
      }
    )

    liked_posts_data_2 = [response.Post(**d) for d in liked_posts_res_2.json()]

    self.assertGreater(len(liked_posts_data_2), 0)

    searched_posts_2 = filter(lambda p: p.id == post_id, liked_posts_data_2)

    self.assertGreater(len(list(searched_posts_2)), 0)

    for item in searched_posts_2:
      self.assertEqual(item.author.first_name, register_data.first_name) # type: ignore
      self.assertEqual(item.author.last_name, register_data.last_name) # type: ignore
      self.assertEqual(item.author.email, register_data.email) # type: ignore        

    settings = request.Settings(
      posts_per_page=30, 
      display_email=True
    )

    settings_res = self.__client.post(
      '/settings/edit?test=true',
      headers={
        'session-code': register_data.session_code
      },
      json=vars(settings)
    )

    self.assertEqual(settings_res.text, 'true')

    post_res_2 = self.__client.get(
      f'/{post_id}?test=true',
      headers={
        'session-code': register_data.session_code
      }
    )

    post_data_2 = response.Post(**post_res_2.json())

    self.assertIs(post_data_2.liked, True)

    self.assertIsNotNone(post_data_2.author)
    self.assertEqual(post_data_2.author.email, user.email) # type: ignore

    post_delete_like_res = self.__client.post(
      '/like/delete?test=true',
      headers={
        'session-code': register_data.session_code
      },
      json=post_id
    )

    self.assertEqual(post_delete_like_res.text, 'true')

    liked_posts_res_3 = self.__client.get(
      "/liked?test=true",
      headers={
        'session-code': register_data.session_code
      }
    )

    liked_posts_data_3 = [response.Post(**d) for d in liked_posts_res_3.json()]

    self.assertEqual(len(liked_posts_data_3), 0)

    post_res_3 = self.__client.get(
      f'/{post_id}?test=true',
      headers={
        'session-code': register_data.session_code
      }
    )

    post_data_3 = response.Post(**post_res_3.json())

    self.assertIs(post_data_3.liked, False)

if __name__ == '__main__':
  unittest.main()
