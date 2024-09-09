import sqlite3, pandas as pd

class SqliteDB:
  def __init__(self, db_file):
    self.db_file = db_file
    self.conn = self.connect()
    self.cur = None

  def connect(self):
    return sqlite3.connect(self.db_file, check_same_thread=False)

  def __del__(self):
    print('sqlite destructor')
    if self.conn:
      self.conn.close()
      self.conn=None
    if self.cur:
      self.cur.close()
      self.cur=None

  def execute(self, query, params=None):
    self.cur = self.conn.cursor()
    if params is None:
      self.cur.execute(query)
    else:
      self.cur.execute(query, params)
    return self.cur

  def table_as_pd(self, table_name:str):
    return self.query_as_pd(f"SELECT * FROM {table_name}")

  def query_as_pd(self, query, params=None):
    return pd.read_sql_query(query, self.conn, params=params)

if __name__ == "__main__":
   print('*** main ***')
   # from utils import download_url, unzip
   import utils as ut
   import os

   db_file='legalAI.db'
   if not os.path.exists(db_file):
      if not os.path.exists('legalsqlite.zip'):
        ut.download_url('https://legalai.commonweb.net/shared_datas/legalsqlite.zip')
      ut.unzip('legalsqlite.zip')

   legalai = SqliteDB(db_file)

   df_test=legalai.table_as_pd('test')

   print(df_test)