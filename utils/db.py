import os
import psycopg

def connect() -> psycopg.Connection:
  return psycopg.connect(
    dbname=os.getenv("POSTGRESQL_DB"), 
    user=os.getenv("POSTGRESQL_USER"),
    password=os.getenv("POSTGRESQL_PWD"),
    host=os.getenv("POSTGRESQL_HOST")
  )
