import os
import sys

sys.path.append(os.getcwd())

from uuid import uuid1
import unittest

from utils import db
import repository.postgresql
from models import data
from constants import SETTINGS_DISPLAY_EMAIL, SETTINGS_POSTS_PER_PAGE

class TestDB(unittest.TestCase):
  __user_repository: repository.postgresql.User
  __session_repository: repository.postgresql.Session
  __post_repository: repository.postgresql.Post
  __like_repository: repository.postgresql.Like

  def setUp(self):
    self.__user_repository = repository.postgresql.User()
    self.__session_repository = repository.postgresql.Session(self.__user_repository)
    self.__post_repository = repository.postgresql.Post()
    self.__like_repository = repository.postgresql.Like()

  def test_user(self):
    user = data.User(
      first_name='__test_1__',
      last_name='__test_1__',
      email='__test_1__@1.again',
      password='test1'
    )

    with db.connect() as conn:
      self.__user_repository.create_wc(user, conn)

      self.assertGreater(user.id, 0)
      self.assertGreater(user.settings.id, 0)    

      user_id = self.__user_repository.get_id_wc(user.email, user.password, conn) # type: ignore

      self.assertEqual(user_id, user.id)

      user_settings = self.__user_repository.get_user_settings_wc(user.id, conn)

      self.assertEqual(user_settings.id, user.id) # type: ignore
      self.assertEqual(user_settings.first_name, user.first_name) # type: ignore
      self.assertEqual(user_settings.last_name, user.last_name) # type: ignore
      
      if SETTINGS_DISPLAY_EMAIL:
        self.assertEqual(user_settings.email, user.email) # type: ignore
      else:
        self.assertIsNone(user_settings.email) # type: ignore

      self.assertEqual(user_settings.settings.id, user.settings.id) # type: ignore
      self.assertEqual(user_settings.settings.user_id, user.id) # type: ignore
      self.assertEqual(user_settings.settings.display_email, SETTINGS_DISPLAY_EMAIL) # type: ignore
      self.assertEqual(user_settings.settings.posts_per_page, SETTINGS_POSTS_PER_PAGE) # type: ignore

      user_settings.settings.posts_per_page = 30 # type: ignore
      user_settings.settings.display_email = True # type: ignore

      settings_edit_result = self.__user_repository.edit_wc(user_settings.settings, conn) # type: ignore

      self.assertTrue(settings_edit_result)

      user_settings_2 = self.__user_repository.get_user_settings_wc(user.id, conn)      

      self.assertEqual(user_settings_2.email, user.email) # type: ignore
      self.assertEqual(user_settings_2.settings.display_email, user_settings.settings.display_email) # type: ignore
      self.assertEqual(user_settings_2.settings.posts_per_page, user_settings.settings.posts_per_page) # type: ignore

      conn.rollback()

  def test_session(self):
    user = data.User(
      first_name='__test_2__',
      last_name='__test_2__',
      email='__test_2__@2.again',
      password='test2'
    )

    with db.connect() as conn:
      user_id = self.__user_repository.create_wc(user, conn)

      self.assertGreater(user_id, 0) # type: ignore

      code = str(uuid1())

      session_id = self.__session_repository.create_wc(user_id, code, conn) # type: ignore

      self.assertGreater(session_id, 0) # type: ignore

      user_settings = self.__session_repository.get_user_settings_wc(session_id, conn) # type: ignore

      self.assertEqual(user_settings.id, user.id) # type: ignore
      self.assertEqual(user_settings.first_name, user.first_name) # type: ignore
      self.assertEqual(user_settings.last_name, user.last_name) # type: ignore
      
      if SETTINGS_DISPLAY_EMAIL:
        self.assertEqual(user_settings.email, user.email) # type: ignore
      else:
        self.assertIsNone(user_settings.email) # type: ignore

      self.assertEqual(user_settings.settings.id, user.settings.id) # type: ignore
      self.assertEqual(user_settings.settings.user_id, user.id) # type: ignore
      self.assertEqual(user_settings.settings.display_email, SETTINGS_DISPLAY_EMAIL) # type: ignore
      self.assertEqual(user_settings.settings.posts_per_page, SETTINGS_POSTS_PER_PAGE) # type: ignore

      session_id_by_code = self.__session_repository.get_id_by_code_wc(code, conn)

      self.assertEqual(session_id_by_code, session_id)

      conn.rollback()

  def test_post(self):
    user = data.User(
      first_name='__test_3__',
      last_name='__test_3__',
      email='__test_3__@1.again',
      password='test3'
    )

    with db.connect() as conn:
      user_id = self.__user_repository.create_wc(user, conn)

      self.assertGreater(user_id, 0) # type: ignore

      post = data.Post(
        title='__title_1',
        text='__text_1',
        abstract='__abstract_1',
        liked=False,
        author=None
      )

      post_id = self.__post_repository.create_wc(user_id, post, conn)

      self.assertGreater(post_id, 0) # type: ignore

      post_by_id = self.__post_repository.get_wc(post_id, user_id, conn) # type: ignore

      self.assertEqual(post_by_id.id, post_id) # type: ignore
      self.assertEqual(post_by_id.title, post.title) # type: ignore
      self.assertEqual(post_by_id.text, post.text) # type: ignore
      self.assertEqual(post_by_id.abstract, post.abstract) # type: ignore
      self.assertEqual(post_by_id.liked, post.liked) # type: ignore

      self.assertEqual(post_by_id.author.id, user.id) # type: ignore
      self.assertEqual(post_by_id.author.first_name, user.first_name) # type: ignore
      self.assertEqual(post_by_id.author.last_name, user.last_name) # type: ignore
      
      if SETTINGS_DISPLAY_EMAIL:
        self.assertEqual(post_by_id.author.email, user.email) # type: ignore
      else:
        self.assertIsNone(post_by_id.author.email) # type: ignore

      posts_list = self.__post_repository.list_wc(user_id, conn)

      self.assertGreater(len(posts_list), 0)

      searched_posts = filter(lambda p: p.id == post_id, posts_list)

      self.assertGreater(len(list(searched_posts)), 0)

      liked_posts_list = self.__post_repository.liked_list_wc(user_id, conn)

      self.assertEqual(len(liked_posts_list), 0)

      self.__like_repository.create_wc(user_id, post_id, conn) # type: ignore

      post_by_id_2 = self.__post_repository.get_wc(post_id, user_id, conn) # type: ignore

      self.assertEqual(post_by_id_2.liked, True) # type: ignore

      posts_list_2 = self.__post_repository.list_wc(user_id, conn)

      searched_posts_2 = filter(lambda p: p.id == post_id, posts_list_2)

      for item in searched_posts_2:
        self.assertEqual(item.liked, True)

      liked_posts_list_2 = self.__post_repository.liked_list_wc(user_id, conn)

      self.assertEqual(len(liked_posts_list_2), 1)

      conn.rollback()
