# создадим в этом файле сессию:
# с помощью которой мы будем 
# отправлять запросы в базу данных и получать ответы.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# URL from ElephantSQL, только postgres://  заменить на postgresql://
engine = create_engine('postgresql://vtfkyays:nICzM7An7TKhf268cBnsmkkLZFkh1eJE@mouse.db.elephantsql.com/vtfkyays')
# показываем, к какой БД хотим подсключиться
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()