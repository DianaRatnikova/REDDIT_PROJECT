import csv
import logging
import os
import time
import app.config
import app.config_auth
from app.db import db_session
from app.print_reddit_data import mkdir_for_results
from app.models import Subreddit, Comment
from datetime import datetime, timedelta

def read_csv(filename, fields):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fields, delimiter=';')
        subreddit_data = list(reader)
        return subreddit_data


def save_top_subreddit(all_data):
    processed = []
    top_subreddit_unique = []
    top_subreddit = {}
    query_url = db_session.query(Subreddit.url_subreddit).distinct()
    urls = []
    for url_addr in query_url:
        urls.append(url_addr[0])

    print("urls = ", '\n'.join(urls))

    for row in all_data:
        subreddit_loaded = 0 # 'False'
        if row['url_subreddit'] not in processed:
            top_subreddit = {'subreddit': row['subreddit'],
                            'author_subreddit': row['author_subreddit'],
                            'url_subreddit': row['url_subreddit'], 
                            'title': row['title'], 
                            'edition_num': row['edition_num']
                            }

            processed.append(top_subreddit['url_subreddit'])
            subreddit_loaded = 0  #'False'
            if not urls or top_subreddit['url_subreddit'] not in urls:
                subreddit_loaded = 1 #'True'
                top_subreddit_unique.append(top_subreddit)
  

    logging.info(f"{top_subreddit_unique = }")

# return_defaults=True говорит bulk_insert_mappings, 
# что когда база присвоит компаниям id, их нужно добавить в top_subreddit_unique.
    db_session.bulk_insert_mappings(Subreddit, top_subreddit_unique, return_defaults=True)
    db_session.commit()

    return top_subreddit_unique


# перебирает список уникальных сабрэддитов и, 
# когда находит нужный, возвращает идентификатор:
def get_top_subreddit_id(url_subreddit, top_subreddit_unique):
    for row in top_subreddit_unique:
        if 'url_subreddit' in row:
            if row['url_subreddit'] == url_subreddit:
                return row['id']
    return None

def get_comment_id(identificator, comments_unique):
    for row in comments_unique:
        if row['identificator'] == identificator:
            return row['id']
    return None

def save_comments(all_data):
    processed = []
    comments_unique = []

    query_id = db_session.query(Comment.identificator).distinct()
    identificators = []
    for id in query_id:
        identificators.append(id[0])

    query_num = db_session.query(Comment.edition_num).distinct()
    numbers_of_edition = []
    for num in query_num:
        numbers_of_edition.append(num[0])    

    query_url = db_session.query(Subreddit.url_subreddit).distinct() 
    
    edit_dict = {}
    for id in identificators:
        query_num_edit = db_session.query(Comment.edition_num).filter(Comment.identificator == id)   #.distinct()
        num_edit_list = []
        for num_edit in query_num_edit:
	        num_edit_list.append(num_edit[0])
        edit_dict[id] = num_edit_list
 

    for row in all_data:
        if row['identificator'] not in processed:
            comment = {'author_comment': row['author_comment'], 
                        'body': row['body'], 
                        'mood': '', 
                        'url_comment': row['url_comment'], 
                        'identificator': row['identificator'],
                        'edition_num': row['edition_num'],
                        'nesting': row['nesting'],
              }

            comment['top_subreddit_id'] = db_session.query(Subreddit.id).filter(Subreddit.url_subreddit == comment['url_comment']).first()[0]
            processed.append(row['identificator'])
# Новый комент
        if not identificators or comment['identificator'] not in identificators:
            comments_unique.append(comment)
        elif identificators:
# Отредактированный коммент
            if int(comment['edition_num']) not in edit_dict[comment['identificator']]:
                    comments_unique.append(comment)
 
    db_session.bulk_insert_mappings(Comment, comments_unique, return_defaults=True)
    db_session.commit()

    return comments_unique



def make_comment_id_dict(identificator, comments_unique):
    comment_id_dict ={}
    for row in comments_unique:
        if row['identificator'] == identificator:
            comment_id_dict[row['identificator']] = row['id']
            return row['id']
    return comment_id_dict


def load_data_to_models():
    logging.info('Reading csv files...')
    mkdir_for_results(app.config_auth.FOLDER_NAME)
    subreddit_data = read_csv(app.config.filename_subreddits, app.config.fields_of_one_subreddit_csv)
    comments_edits_data = read_csv(app.config.filename_comments_edition, app.config.fields_of_comments_edits_csv)
    os.chdir("..")
    logging.info('End reading')  

    logging.info('Saving subreddits to database...')
    top_subreddits = save_top_subreddit(subreddit_data)
    logging.info('Saving comments to database...')
    comments = save_comments(comments_edits_data)
if __name__ == '__main__':
    load_data_to_models()
