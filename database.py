from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL to connect to your MySQL database.
DATABASE_URL = "mysql+pymysql://root:my_password@127.0.0.1:3307/contacts_db"

# Creating the database engine
# echo=True; it prints SQL statements in the terminal
engine = create_engine(DATABASE_URL, echo=True)

# used to interact with the database by creating session factory
# autocommit=False:changes will not save automtically
# autoflush=False: avoid sending changes to database automatically 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining tables
Base = declarative_base()
