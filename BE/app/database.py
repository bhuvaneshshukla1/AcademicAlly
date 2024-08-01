from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from app.config import CLOUD_SQL_CONNECTION_NAME, DB_USER, DB_PASSWORD, DB_NAME

def get_conn():
  connector = Connector()
  conn = connector.connect(
      CLOUD_SQL_CONNECTION_NAME,
      "pymysql",
      user=DB_USER,
      password=DB_PASSWORD,
      db=DB_NAME,
      ip_type=IPTypes.PUBLIC
  )
  return conn

def create_engine():
  pool = sqlalchemy.create_engine(
      "mysql+pymysql://",
      creator=get_conn
  )
  return pool