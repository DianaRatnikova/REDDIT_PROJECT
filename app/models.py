from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime

from app.db import Base, engine
import datetime
from sqlalchemy.orm import relationship


class Subreddit(Base):
    #название таблицы не должно совпадать с именем класса!!
    __tablename__ = 'subreddits'
    id = Column(Integer, primary_key=True)
    subreddit = Column(String)
    author_subreddit = Column(String)
    title = Column(String)
    url_subreddit = Column(String)
    comments = relationship("Comment", lazy="joined")
    comment_edition = relationship("CommentEdition", lazy="joined")
    data_loaded = relationship("LoadingInfo", lazy="joined")
    def __repr__(self):
        return f'Subreddit id: {self.id}, author: {self.author}'


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    top_subreddit_id = Column(Integer, ForeignKey(Subreddit.id), index=True, nullable=False)
    author_comment = Column(String)
    body = Column(String)
    mood = Column(String)
    url_comment = Column(String)
    nesting = Column(Integer)
    identificator = Column(String)
    top_subreddits = relationship("Subreddit")
    comment_edition = relationship("CommentEdition", lazy="joined")
    data_loaded = relationship("LoadingInfo", lazy="joined")
  #  comments_edit =  relationship("Comments_edit", lazy="joined")
    def __repr__(self):
        return f'Comment id: {self.id}, author: {self.author}'


class CommentEdition(Base):
    __tablename__ = 'comment_editions'

    id = Column(Integer, primary_key=True)
    top_subreddit_id = Column(Integer, ForeignKey(Subreddit.id), index=True, nullable=False)
    comment_id = Column(Integer, ForeignKey(Comment.id), index=True, nullable=False)
    body = Column(String)
    mood = Column(String)
    url_comment = Column(String)
    identificator_comment = Column(String)
    edition_num = Column(Integer)
    top_subreddits = relationship("Subreddit")
    comments = relationship("Comment")
    def __repr__(self):
        return f'Comment_edit id: {self.id}, identificator_comment: {self.identificator_comment}'


class LoadingInfo(Base):
    __tablename__ = 'loading_info'

    id = Column(Integer, primary_key=True)
    subreddit_id = Column(Integer, ForeignKey(Subreddit.id), index=True, nullable=False)
    comment_id = Column(Integer, ForeignKey(Comment.id), index=True, nullable=False)
    comment_edition_id = Column(Integer, ForeignKey(CommentEdition.id), index=True, nullable=False)
    subreddit_loaded = Column(Boolean)
    date_loaded = Column(DateTime, default=datetime.datetime.utcnow)
    top_subreddits = relationship("Subreddit", lazy="joined")
    comment_edition = relationship("CommentEdition", lazy="joined")
    comments = relationship("Comment", lazy="joined")
    def __repr__(self):
        return f'Data_loaded id: {self.id}, date_loaded: {self.date_loaded}'

def create_models():
    Base.metadata.create_all(bind=engine)    

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)