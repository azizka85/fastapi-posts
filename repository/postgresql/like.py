import psycopg
from utils import db

import repository

class Like(repository.Like):
  def create(self, user_id: int, post_id: int):
    with db.connect() as conn:
      self.create_wc(user_id, post_id, conn)

  def create_wc(self, user_id: int, post_id: int, conn: psycopg.Connection):
    conn.execute(
      '''
        insert into likes(user_id, post_id) 
        values (%(user_id)s, %(post_id)s);
      ''',
      {'user_id': user_id, 'post_id': post_id}
    )

  def delete(self, user_id: int, post_id: int):
    with db.connect() as conn:
      self.delete_wc(user_id, post_id, conn)

  def delete_wc(self, user_id: int, post_id: int, conn: psycopg.Connection):
    conn.execute(
      '''
        delete from 
          likes 
        where 
          user_id = %(user_id)s
          and post_id = %(post_id)s;
      ''',
      {'user_id': user_id, 'post_id': post_id}
    )
