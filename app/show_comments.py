import app.config_auth
from app.db import db_session
from app.models import Subreddit, Comment
from app.print_reddit_data import mkdir_for_results
import logging
import os
from pprint import pprint

# из таблицы комментов вытаскиваем все ид сабреддитов
def get_subreddit_id_from_comments_db1():
    query_subreddits_id = db_session.query(Comment.top_subreddit_id).distinct()
    subreddit_id_list = []
    for subreddit_id in query_subreddits_id:
        subreddit_id_list.append(subreddit_id[0])
    return subreddit_id_list


# из таблицы комментов вытаскиваем все ид сабреддитов
def get_subreddit_id_from_comments_db():
    query_subreddits_id = db_session.query(Comment.top_subreddit_id).distinct()
    subreddit_id_list = [subreddit_id[0] for subreddit_id in query_subreddits_id]
    return subreddit_id_list

def get_comments_identificators(subreddit_id, subreddit_id_comments_identificator):
    query_identificators = db_session.query(Comment.identificator).\
                            filter(Comment.top_subreddit_id == subreddit_id).distinct()
    comments_identificator_list = [identificator[0] for identificator in query_identificators]
    subreddit_id_comments_identificator[subreddit_id] = comments_identificator_list


# подсчёт количества уникальных сабрэддитов
def distinct_subreddits():
    subreddits_count = db_session.query(Comment.top_subreddit_id).\
                        group_by(Comment.top_subreddit_id).count()
    print(f"There are {subreddits_count} subreddits in the database\n")


# подсчёт количества уникальных комментариев для каждого сабрэддита
def distinct_comments(subreddit_id):
    comments_count = db_session.query(Comment.identificator).\
                        filter(Comment.top_subreddit_id == subreddit_id).\
                        group_by(Comment.identificator).count()
    mkdir_for_results(app.config_auth.FOLDER_NAME)
    with open('edits_story.txt', 'a', encoding='utf-8') as file_edit:
        file_edit.write(f"Subreddit {subreddit_id} has {comments_count} comments\n")
    os.chdir("..")  


# "Comment {comment_identificator} has {edition_count-1} edits
def distinct_editions(subreddit_id, comment_identificator):
    edition_count = db_session.query(Comment.edition_num).\
                    filter(Comment.top_subreddit_id == subreddit_id).\
                    filter(Comment.identificator== comment_identificator).\
                    group_by(Comment.edition_num).count()
    return edition_count

def show_comments():
    distinct_subreddits()

    logging.info("Showing comments: ")
    subreddit_id_list = get_subreddit_id_from_comments_db()

    for subreddit_id in subreddit_id_list:
        distinct_comments(subreddit_id)

    subreddit_id_comments_identificator = {}
    for subreddit_id in subreddit_id_list:
        get_comments_identificators(subreddit_id, subreddit_id_comments_identificator)

    for subreddit_id in subreddit_id_list:
        subreddit_text = db_session.query(Subreddit.title).\
                        filter(Subreddit.id == subreddit_id).first()
        mkdir_for_results(app.config_auth.FOLDER_NAME)
        with open('edits_story.txt', 'a', encoding='utf-8') as file_edit:
            file_edit.write(f"\n----------------------------------------")
            file_edit.write(f"\n{subreddit_text = }\n")
        os.chdir("..")                        
        for comment_identificator in subreddit_id_comments_identificator[subreddit_id]:
            edition_count = distinct_editions(subreddit_id, comment_identificator)
            if edition_count>1:
                query = db_session.query(Subreddit, Comment).\
                    join(Subreddit, Comment.top_subreddit_id == Subreddit.id).\
                    filter(Comment.top_subreddit_id == subreddit_id).\
                    filter(Comment.identificator == comment_identificator).\
                    order_by(Comment.edition_num.desc())
                for subreddit, comment in query:
                    mkdir_for_results(app.config_auth.FOLDER_NAME)
                    with open('edits_story.txt', 'a', encoding='utf-8') as file_edit:
                        file_edit.write(f"{comment.author_comment = }\n{comment.body = }\n\n")
                    os.chdir("..")  

