from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv('PASSWORD')
LOCALHOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')


MYSQL_DATABASE_URL = f'mysql+pymysql://root:{PASSWORD}@{LOCALHOST}:{PORT}/{DATABASE}'

engine = create_engine(MYSQL_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
