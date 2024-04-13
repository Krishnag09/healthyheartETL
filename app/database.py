import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# db_path = os.path.abspath("../healthyheartDB")
# db_url = f"jdbc:sqlite:{db_path}"
#
#
# engine = create_engine(db_url)
#
# Session = sessionmaker(bind=engine)
