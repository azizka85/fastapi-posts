from typing import Union

import psycopg
from psycopg.rows import dict_row

from utils import db

from models import data
import repository
from repository.postgresql.user import User as UserRepository

class Session(repository.Session):
  __user_repository: UserRepository

  def __init__(self, user_repository: UserRepository):
    self.__user_repository = user_repository

  def create(self, user_id: int, code: str) -> Union[int, None]:
    id = None

    with db.connect() as conn:
      id = self.create_wc(user_id, code, conn)

    return id

  def create_wc(self, user_id: int, code: str, conn: psycopg.Connection) -> Union[int, None]:
    id = None

    cur = conn.execute(
      '''
        insert into sessions(user_id, code) 
        values (%(user_id)s, %(code)s)
        returning id;
      ''',
      {'user_id': user_id, 'code': code}
    )

    record = cur.fetchone()

    if record:
      id = record[0]

    return id
  
  def get_user_settings(self, session_id: int) -> Union[data.User, None]:
    user = None

    with db.connect() as conn:
      user = self.get_user_settings_wc(session_id, conn)

    return user
  
  def get_user_settings_wc(self, session_id: int, conn: psycopg.Connection) -> Union[data.User, None]:
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
          users u, settings s, sessions t
        where
          s.user_id = u.id
          and u.id = t.user_id
          and t.id = %(id)s;
      ''',
      {'id': session_id}
    )

    cur.row_factory = dict_row
    record = cur.fetchone()

    if record:
      user =  self.__user_repository.read(record)

    return user

  def get_id_by_code(self, session_code: str) -> Union[int, None]:
    id = None

    with db.connect() as conn:
      id = self.get_id_by_code_wc(session_code, conn)

    return id
  
  def get_id_by_code_wc(self, session_code: str, conn: psycopg.Connection) -> Union[int, None]:
    id = None

    cur = conn.execute(
      '''
        select
          id
        from 
          sessions
        where 
          code = %(code)s;
      ''',
      {'code': session_code}
    )

    record = cur.fetchone()

    if record:
      id = record[0]

    return id
