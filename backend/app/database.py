from dotenv import load_dotenv
load_dotenv()
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# INSTANCIATING A DATABASE FRAMEWORK (i.e. a mix of container and base class) 
MyDB = declarative_base()

def get_connection_uri():
    # Read URI parameters from the environment or use default values
    dbhost = os.getenv('DBHOST', 'localhost')  # Default to 'localhost'
    dbname = os.getenv('DBNAME', 'mydatabase')  # Default database name
    dbuser = urllib.parse.quote(os.getenv('DBUSER', 'myuser'))  # Default user
    password = urllib.parse.quote(os.getenv('PASSWORD', 'mypassword'))  # Default password

    # Create the connection URI
    db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}"
    return db_uri

URL_DATA_BASE = get_connection_uri()


def db_connect(url: str = URL_DATA_BASE, **kwargs):
    """
    Creates or updates the database schema then returns access to it.

    The database itself is never overwritten but only udpdated or created when
    not already in place. The same for the tables inside the database.

    Parameter(s):
        url (str): url to connect the choosen database.
                   By default: "sqlite:///../simplon.db"
        **kwargs : Additional arguments to be passed to `create_engine` method.
                   For any details about the said method, see SQLAlchemy doc.
                   Example: It is possible

    Returns:
        A SQLAlchemy `sessionmaker` object to be instanciated into sessions.
    """
    # SET THE DB TYPE (sqlite, PostgreSQL, etc.) AND AN ENGINE (i.e. connector)
    engine = create_engine(url, **kwargs)

    # CREATES THE REQUIRED DATABASE (according data given into `url`)
    
    MyDB.metadata.create_all(engine, checkfirst=True)

    # FUNCTION OUTPUT (returns a `sessionmaker` object to help DB interactions)
    return sessionmaker(bind=engine)

SessionLocal = db_connect()


def get_db():
    """
    Returns a database session.

    Returns:
        SessionLocal: The database session.

    Yields:
        SessionLocal: The database session.

    Raises:
        None

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()