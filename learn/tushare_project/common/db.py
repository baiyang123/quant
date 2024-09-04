from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()


def get_session(db_id='quant'):
    engine = db.get_engine(bind=db_id).connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# BaseModel = declarative_base()