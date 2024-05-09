from typing import Any, Dict, Union
import hashlib

import psycopg
from psycopg.rows import dict_row

from utils import db

from models import data
import repository

class User(repository.User):
  def create(self, user: data.User) -> Union[int, None]:
    id = None

    with db.connect() as conn:
      id = self.create_wc(user, conn)      

    return id
  
  def create_wc(self, user: data.User, conn: psycopg.Connection) -> Union[int, None]:
    id = self.create_user_wc(user, conn)

    if id:
      user.id = id
      user.settings.user_id = id

    settings_id = self.create_settings_wc(user.settings, conn)

    if settings_id:
      user.settings.id = settings_id

    return id

  def create_user_wc(self, user: data.User, conn: psycopg.Connection) -> Union[int, None]:
    id = None
    pwd = str(hashlib.md5(user.password.encode())) # type: ignore

    cur = conn.execute(
      '''
        insert into users(first_name, last_name, email, password) 
        values (%(first_name)s, %(last_name)s, %(email)s, %(pwd)s)
        returning id;
      ''',
      {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'pwd': pwd}
    )

    record = cur.fetchone()

    if record:
      id = record[0]

    return id
  
  def create_settings_wc(self, settings: data.Settings, conn: psycopg.Connection) -> Union[int, None]:
    id = None

    cur = conn.execute(
      '''
        insert into settings(user_id, posts_per_page, display_email) 
        values (%(user_id)s, %(posts_per_page)s, %(display_email)s)
        returning id;
      ''',
      {'user_id': settings.user_id, 'posts_per_page': settings.posts_per_page, 'display_email': settings.display_email}
    )

    record = cur.fetchone()

    if record:
      id = record[0]

    return id

  def get_id(self, email: str, pwd: str) -> Union[int, None]:
    id = None

    with db.connect() as conn:
      id = self.get_id_wc(email, pwd, conn)

    return id
  
  def get_id_wc(self, email: str, password: str, conn: psycopg.Connection) -> Union[int, None]:
    id = None
    pwd = str(hashlib.md5(password.encode()))

    cur = conn.execute(
      '''
        select
          id
        from 
          users
        where 
          email = %(email)s
          and password = %(pwd)s;
      ''',
      {'email': email, 'pwd': pwd}
    )

    record = cur.fetchone()

    if record:
      id = record[0]

    return id
  
  def get_user_settings(self, id: int) -> Union[data.User, None]:
    user = None

    with db.connect() as conn:
      user = self.get_user_settings_wc(id, conn)

    return user
  
  def get_user_settings_wc(self, id: int, conn: psycopg.Connection) -> Union[data.User, None]:
    user = None

    cur = conn.execute(
      '''
        select 
          u.id user_id, u.first_name, u.last_name, 
          case
            when s.display_email = false then null
            else u.email
          end email, 
          s.id settings_id, s.posts_per_page, s.display_email
        from
          users u, settings s
        where
          s.user_id = u.id
          and u.id = %(id)s;
      ''',
      {'id': id}
    )

    cur.row_factory = dict_row
    record = cur.fetchone()

    if record:
      user =  self.read(record)

    return user
  
  def edit(self, settings: data.Settings) -> bool:
    result = False

    with db.connect() as conn:
      result = self.edit_wc(settings, conn)

    return result
  
  def edit_wc(self, settings: data.Settings, conn: psycopg.Connection) -> bool:
    conn.execute(
      '''
        update 
          settings 
        set
          posts_per_page = %(posts_per_page)s,
          display_email = %(display_email)s
        where
          user_id = %(user_id)s;
      ''',
      {'user_id': settings.user_id, 'posts_per_page': settings.posts_per_page, 'display_email': settings.display_email}
    )

    return True

  def read(self, record: Dict[str, Any]) -> data.User:
    user = data.User(
      first_name=record['first_name'],
      last_name=record['last_name'],
      email=record['email'],
      password=None
    )

    user.id = record['user_id']
    user.settings.id = record['settings_id']
    user.settings.user_id = user.id
    user.settings.display_email = record['display_email']
    user.settings.posts_per_page = record['posts_per_page']

    return user
