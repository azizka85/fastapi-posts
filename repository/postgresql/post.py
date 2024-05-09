from typing import Any, Dict, List, Union

import psycopg
from psycopg.rows import dict_row

from utils import db

from models import data
import repository

class Post(repository.Post):
  def create(self, user_id: Union[int, None], post: data.Post) -> Union[int, None]:
    id = None

    with db.connect() as conn:
      id = self.create_wc(user_id, post, conn)    

    return id
  
  def create_wc(self, user_id: Union[int, None], post: data.Post, conn: psycopg.Connection) -> Union[int, None]:
    id = None

    cur = conn.execute(
      '''
        insert into posts(user_id, title, text, abstract)
        values (%(user_id)s, %(title)s, %(text)s, %(abstract)s)
        returning id;
      ''',
      {'user_id': user_id, 'title': post.title, 'text': post.text, 'abstract': post.abstract}
    )

    record = cur.fetchone()

    if record:
      id = record[0]

    if id:
      post.id = id

    return id
  
  def get(self, id: int, user_id: Union[int, None]) -> Union[data.Post, None]:
    post = None

    with db.connect() as conn:
      post = self.get_wc(id, user_id, conn)  

    return post
  
  def get_wc(self, id: int, user_id: Union[int, None], conn: psycopg.Connection) -> Union[data.Post, None]:
    post = None

    cur = conn.execute(
      '''
        select 
          u.id user_id, u.first_name, u.last_name,
          case
            when s.display_email is null or s.display_email = false then null
            else u.email
          end email,
          p.id post_id, p.title, p.text, p.abstract,
          case
            when l.id is null then false
            else true
          end liked
        from 
          posts p
        left join
          users u 
          on p.user_id = u.id
        left join 
          settings s
          on p.user_id = s.user_id
        left join
          likes l
          on p.id = l.post_id
            and l.user_id = %(user_id)s
        where
          p.id = %(id)s;
      ''',
      {'id': id, 'user_id': user_id}
    )

    cur.row_factory = dict_row
    record = cur.fetchone()

    if record:
      post =  self.read(record)

    return post
  
  def list(self, user_id: Union[int, None]) -> List[data.Post]:
    res = []

    with db.connect() as conn:
      res = self.list_wc(user_id, conn)

    return res
  
  def list_wc(self, user_id: Union[int, None], conn: psycopg.Connection) -> List[data.Post]:
    res = []

    cur = conn.execute(
      '''
        select 
          u.id user_id, u.first_name, u.last_name,
          case
            when s.display_email is null or s.display_email = false then null
            else u.email
          end email,
          p.id post_id, p.title, p.text, p.abstract,
          case
            when l.id is null then false
            else true
          end liked
        from 
          posts p
        left join
          users u 
          on p.user_id = u.id
        left join 
          settings s
          on p.user_id = s.user_id
        left join
          likes l
          on p.id = l.post_id
            and l.user_id = %(user_id)s;
      ''',
      {'user_id': user_id}
    )

    cur.row_factory = dict_row

    for record in cur:
      res.append(
        self.read(record)
      )

    return res
  
  def liked_list(self, user_id: Union[int, None]) -> List[data.Post]:
    res = []

    with db.connect() as conn:
      res = self.liked_list_wc(user_id, conn)

    return res
  
  def liked_list_wc(self, user_id: Union[int, None], conn: psycopg.Connection) -> List[data.Post]:
    res = []

    cur = conn.execute(
      '''
        select 
          u.id user_id, u.first_name, u.last_name,
          case
            when s.display_email is null or s.display_email = false then null
            else u.email
          end email,
          p.id post_id, p.title, p.text, p.abstract,
          case
            when l.id is null then false
            else true
          end liked
        from 
          posts p
        left join
          users u 
          on p.user_id = u.id
        left join 
          settings s
          on p.user_id = s.user_id
        inner join
          likes l
          on p.id = l.post_id
            and l.user_id = %(user_id)s;
      ''',
      {'user_id': user_id}
    )

    cur.row_factory = dict_row

    for record in cur:
      res.append(
        self.read(record)
      )

    return res

  def read(self, record: Dict[str, Any]) -> data.Post:
    post = data.Post(
      title=record['title'],
      text=record['text'],
      abstract=record['abstract'],
      liked=record['liked'],
      author=None      
    )

    post.id = record['post_id']
    
    if record['user_id']:
      post.author = data.User(
        first_name=record['first_name'],
        last_name=record['last_name'],
        email=record['email'],
        password=None
      )

      post.author.id = record['user_id']

    return post
