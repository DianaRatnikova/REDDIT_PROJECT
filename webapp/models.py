from sqlalchemy import Column, Integer, String, Date, ForeignKey

from webapp.db import Base, engine
from sqlalchemy.orm import relationship


class Top_subreddits(Base):
    #название таблица не должно совпадать с именем класса!!
    __tablename__ = 'top_subreddit'
    id = Column(Integer, primary_key=True)
    subreddit = Column(String)
    author_subreddit = Column(String)
    title = Column(String)
    url_subreddit = Column(String)
    comments = relationship("Comments", lazy="joined")

    def __repr__(self):
        return f'Top subreddit id: {self.id}, author: {self.author}'


class Comments(Base):
    #название таблица не должно совпадать с именем класса!!
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    top_subreddit_id = Column(Integer, ForeignKey(Top_subreddits.id), index=True, nullable=False)
    author_comment = Column(String)
    body = Column(String)
    mood = Column(String)
    url_comment = Column(String)
    nesting = Column(Integer)
    identificator = Column(String)
    top_subreddits = relationship("Top_subreddits")
  #  comments_edit =  relationship("Comments_edit", lazy="joined")
    def __repr__(self):
        return f'Comment id: {self.id}, author: {self.author}'


class Comments_edit(Base):
    #название таблицы не должно совпадать с именем класса!!
    __tablename__ = 'comments_edits'

    id = Column(Integer, primary_key=True)
  #  comment_id = Column(Integer, ForeignKey(Comments.id), index=True, nullable=False)
    top_subreddit_id = Column(Integer, ForeignKey(Top_subreddits.id), index=True, nullable=False)
    body = Column(String)
    mood = Column(String)
    url_comment = Column(String)
    identificator_comment = Column(String)
    edition_num = Column(Integer)
  #  top_subreddits = relationship("Comments")
    top_subreddits = relationship("Top_subreddits")
    def __repr__(self):
        return f'Comment_edit id: {self.id}, identificator_comment: {self.identificator_comment}'


def create_models():
    Base.metadata.create_all(bind=engine)    

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)