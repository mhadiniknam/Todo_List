import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

required_vars = [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]
if not all(required_vars):
    raise ValueError(
        "One or more database environment variables are missing. "
        "Please check your .env file for DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME."
    )

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """
    A generator function for providing a transactional SQLAlchemy session.
    This handles the commit, rollback, and closing of the session.
    """
    db = SessionFactory()
    try:
        yield db
        db.commit() # Commit the transaction if everything was successful
    except Exception:
        db.rollback() # Roll back the transaction in case of any error
        raise
    finally:
        db.close() # Always close the session