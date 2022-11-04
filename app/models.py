from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime

from app.db import Base, engine
import datetime
from sqlalchemy.orm import relationship


class Subreddit(Base):
    # название таблицы не должно совпадать с именем класса!!
    __tablename__ = 'subreddits'
    id = Column(Integer, primary_key=True)
    subreddit = Column(String)
    author_subreddit = Column(String)
    title = Column(String)
    url_subreddit = Column(String)
    edition_num = Column(Integer)
    comment_edition = relationship("Comment", lazy="joined", primaryjoin="Subreddit.id==Comment.top_subreddit_id", back_populates='top_subreddits')
    def __repr__(self):
    #    return f'Subreddit id: {self.id}, author: {self.author_subreddit}'
        return f'title: {self.title}, \n author: {self.author_subreddit}'


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    top_subreddit_id = Column(Integer, ForeignKey(Subreddit.id), index=True, nullable=False)
    author_comment = Column(String)
    body = Column(String)
    mood = Column(String)
    url_comment = Column(String)
    identificator = Column(String)
    edition_num = Column(Integer)
    top_subreddits = relationship("Subreddit", back_populates='comment_edition')
    def __repr__(self):
    #    return f'Comment id: {self.id}, identificator_comment: {self.identificator}'
        return f'author_comment: {self.author_comment}, \n text: {self.body} \n'


class ActualComment(Base):
    __tablename__ = 'actual_comments'
    id = Column(Integer, primary_key=True)


def create_models():
    Base.metadata.create_all(bind=engine)    

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)