import csv
import logging
import os
import time
import app.config
import app.config_auth
from app.db import db_session
from app.print_reddit_data import mkdir_for_results
from app.models import Subreddit, Comment, CommentEdition, LoadingInfo
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
                            }
            top_subreddit_unique.append(top_subreddit)
            processed.append(top_subreddit['url_subreddit'])
            if not urls or top_subreddit['url_subreddit'] not in urls:
                subreddit_loaded = 1 #'True'
# return_defaults=True говорит bulk_insert_mappings, 
# что когда база присвоит компаниям id, их нужно добавить в top_subreddit_unique.
                db_session.bulk_insert_mappings(Subreddit, top_subreddit_unique, return_defaults=True)
                db_session.commit()
            else:
                id = db_session.query(Subreddit.id).filter(Subreddit.url_subreddit == top_subreddit['url_subreddit']).first()[0]
                if (top_subreddit_unique):
                    top_subreddit_unique[0]['id'] = id
                    logging.info(f"{id = }")
                    
    if (top_subreddit_unique):
        top_subreddit_unique[0]['subreddit_loaded'] = subreddit_loaded

    print(f"{top_subreddit_unique = }")
    logging.info(f"{top_subreddit_unique = }")
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

def save_comments(all_data, top_subreddit_unique):
    processed = []
    comments_unique = []

    query_id = db_session.query(Comment.identificator).distinct()
    identificators = []
    for id in query_id:
        identificators.append(id[0])

    for row in all_data:
        if row['identificator'] not in processed:
            comment = {'author_comment': row['author_comment'], 
                        'body': row['body'], 
                        'mood': '', 
                        'url_comment': row['url_comment'], 
                        'nesting': row['nesting'],
                        'identificator': row['identificator']
              }
            comment['top_subreddit_id'] = get_top_subreddit_id(row['url_comment'], top_subreddit_unique)
            comments_unique.append(comment)
            processed.append(row['identificator'])
 #   logging.info(f"{comments_unique = }")
# Записываем коммент в бд, только если его раньше не было
 #   if not identificators or comment['identificator'] not in identificators:
    db_session.bulk_insert_mappings(Comment, comments_unique, return_defaults=True)
    db_session.commit()
    return comments_unique


def save_comments_edits(all_data,top_subreddit_unique,comments):
    processed = []
    comments_edits_unique = []

    query_id = db_session.query(CommentEdition.identificator_comment).distinct()
    identificators = []
    for id in query_id:
        identificators.append(id[0])

    query_num = db_session.query(CommentEdition.edition_num).distinct()
    numbers_of_edition = []
    for num in query_num:
        numbers_of_edition.append(num[0])

    for row in all_data:
        if row['edition_num'] not in processed:
            comment_edit = {'body': row['body'], 'mood': '', 'identificator_comment': row['identificator_comment'],
            'edition_num': row['edition_num'],'url_comment': row['url_comment'],
            }

            comment_edit['top_subreddit_id'] = get_top_subreddit_id(row['url_comment'], top_subreddit_unique)
            comment_edit['comment_id'] = get_comment_id(row['identificator_comment'], comments)

   #         if not identificators:
            comments_edits_unique.append(comment_edit)
            processed.append(row['edition_num'])
            id_comment_edit = 111
            for id in identificators:
                if comment_edit['identificator_comment'] == id:
                    if int(comment_edit['edition_num']) in numbers_of_edition:
                        print(f"No more edited!  {comment_edit['edition_num'] = }")
                        id_comment_edit = db_session.query(CommentEdition.id).filter(CommentEdition.edition_num == comment_edit['edition_num']).first()[0]
                        comments_edits_unique[0]['id'] = id_comment_edit
                        logging.info(f"{id_comment_edit = }")
                    else:
                        print(f"Edited! {comment_edit['edition_num'] = }")
                        db_session.bulk_insert_mappings(CommentEdition, comments_edits_unique, return_defaults=True)
                        db_session.commit()
    logging.info(f"!!!{id_comment_edit = }")
 #   print(f"{comments_edits_unique = }")
    return comments_edits_unique


def save_loading_info(top_subreddits,comments_edits):
    loading_info = {"date_loaded": str(datetime.now()), 
                    "subreddit_loaded": top_subreddits[0]['subreddit_loaded'],
                    "subreddit_id": top_subreddits[0]['id'], 
                    "comment_edition_id": 12, #comments_edits[0]['id'],
                    "comment_id": comments_edits[0]['comment_id']
    }
    db_session.bulk_insert_mappings(LoadingInfo, loading_info, return_defaults=True)
    db_session.commit()



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
    subreddit_data = read_csv(app.config.filename_top_subreddits, app.config.fields_of_top_subreddit_csv)
    comments_data = read_csv(app.config.filename_comments, app.config.fields_of_comments_csv)
    comments_edits_data = read_csv(app.config.filename_comments_edition, app.config.fields_of_comments_edits_csv)
    os.chdir("..")
    logging.info('End reading')  

    logging.info('Saving subreddits to database...')
    top_subreddits = save_top_subreddit(subreddit_data)
    logging.info('Saving comments to database...')
    comments = save_comments(comments_data, top_subreddits)
    logging.info('Saving comments_edits to database...')
    comments_edits = save_comments_edits(comments_edits_data,top_subreddits,comments)
    logging.info('Saving loaded_data to database...')
    loaded_data = save_loading_info(top_subreddits,comments_edits)
if __name__ == '__main__':
    load_data_to_models()
