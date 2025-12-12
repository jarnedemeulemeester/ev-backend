from .database import Database

db = Database()


def get_db():
    session = db.session()
    try:
        yield session
    finally:
        session.close()
