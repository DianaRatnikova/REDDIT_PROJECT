from sqlalchemy import Column, Integer, String, Date, ForeignKey

from webapp.db import Base, engine
from sqlalchemy.orm import relationship


class Top_subreddits(Base):
    __tablename__ = 'top_subreddits'
    id = Column(Integer, primary_key=True)
    subreddit = Column(String)
    author_subreddit = Column(String)
    title = Column(String)
    url_subreddit = Column(String)
    comments = relationship("Comments", lazy="joined")

    def __repr__(self):
        return f'Top subreddit id: {self.id}, author: {self.author}'


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    top_subreddit_id = Column(Integer, ForeignKey(Top_subreddits.id), index=True, nullable=False)
    author_comment = Column(String)
    body = Column(String)
    mood = Column(String)
    url_comment = Column(String)
    nesting = Column(Integer)
    identificator = Column(String)
    top_subreddits = relationship("Top_subreddits")

    def __repr__(self):
        return f'Comment id: {self.id}, author: {self.author}'

def create_models():
    Base.metadata.create_all(bind=engine)    

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)