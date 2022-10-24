import csv
from webapp.db import db_session
import os
import time
import webapp.config_auth
from webapp.print_reddit_data import mkdir_for_results
from webapp.models import Top_subreddits, Comments, Comments_edit
#from sqlalchemy import distinct
import logging
import webapp.config

def read_csv(filename, fields):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fields, delimiter=';')
        subreddit_data = list(reader)
        return subreddit_data


def read_top_subreddit_csv(filename):
    fields = ['subreddit',  'author_subreddit', 'title', 'url_subreddit']
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fields, delimiter=';')
        subreddit_data = list(reader)
        return subreddit_data


def read_comments_csv(filename):
    fields = ['identificator',  'author_comment', 'body', 'url_comment', 'nesting']    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fields, delimiter=';')
        comments_data = list(reader)
        return comments_data


def read_comments_edits_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['identificator_comment',  'body', 'edition_num','url_comment']
        reader = csv.DictReader(f, fields, delimiter=';')
        comments_edits = list(reader)
        return comments_edits


def save_top_subreddit(all_data):
    processed = []
    top_subreddit_unique = []

    query_url = db_session.query(Top_subreddits.url_subreddit).distinct()
    urls = []
    for url in query_url:
        urls.append(url[0])
    print("urls = ", '\n'.join(urls))

    for row in all_data:
        if row['url_subreddit'] not in processed:
            top_subreddit = {'subreddit': row['subreddit'],'author_subreddit': row['author_subreddit'],
            'url_subreddit': row['url_subreddit'], 'title': row['title'], }

            if not urls or top_subreddit['url_subreddit'] not in urls:
                top_subreddit_unique.append(top_subreddit)
                processed.append(top_subreddit['url_subreddit'])
# return_defaults=True говорит bulk_insert_mappings, 
# что когда база присвоит компаниям id, их нужно добавить в top_subreddit_unique.
    db_session.bulk_insert_mappings(Top_subreddits, top_subreddit_unique, return_defaults=True)
    db_session.commit()
    return top_subreddit_unique


# перебирает список уникальных сабрэддитов и, 
# когда находит нужный, возвращает идентификатор:
def get_top_subreddit_id(url_subreddit, top_subreddit_unique):
    for row in top_subreddit_unique:
        if row['url_subreddit'] == url_subreddit:
            return row['id']
    return None


def save_comments(all_data, top_subreddit_unique):
    processed = []
    comments_unique = []

    query_id = db_session.query(Comments.identificator).distinct()
    identificators = []
    for id in query_id:
        identificators.append(id[0])

    for row in all_data:
        if row['identificator'] not in processed:
            comment = {'author_comment': row['author_comment'], 'body': row['body'], 'mood': '', 
            'url_comment': row['url_comment'], 'nesting': row['nesting'], 'identificator': row['identificator']
              }
            comment['top_subreddit_id'] = get_top_subreddit_id(row['url_comment'], top_subreddit_unique)

            if not identificators or comment['identificator'] not in identificators:
                comments_unique.append(comment)
                processed.append(row['identificator'])

    db_session.bulk_insert_mappings(Comments, comments_unique, return_defaults=True)
    db_session.commit()
    return comments_unique


def save_comments_edits(all_data,top_subreddit_unique):
    processed = []
    comments_edits_unique = []

    query_id = db_session.query(Comments_edit.identificator_comment).distinct()
    identificators = []
    for id in query_id:
        identificators.append(id[0])

    query_num = db_session.query(Comments_edit.edition_num).distinct()
    numbers_of_edition = []
    for num in query_num:
        numbers_of_edition.append(num[0])

    for row in all_data:
        if row['edition_num'] not in processed:
            comment_edit = {'body': row['body'], 'mood': '', 'identificator_comment': row['identificator_comment'],
            'edition_num': row['edition_num'],'url_comment': row['url_comment'],
            }
            comment_edit['top_subreddit_id'] = get_top_subreddit_id(row['url_comment'], top_subreddit_unique)

            if not identificators:
                    comments_edits_unique.append(comment_edit)
                    processed.append(row['edition_num'])

            for id in identificators:
                if comment_edit['identificator_comment'] == id:
                    if int(comment_edit['edition_num']) in numbers_of_edition:
                        print(f"No more edited!  {comment_edit['edition_num'] = }")
                    else:
                        print(f"Edited! {comment_edit['edition_num'] = }")
                        comments_edits_unique.append(comment_edit)
                        processed.append(row['edition_num'])
    db_session.bulk_insert_mappings(Comments_edit, comments_edits_unique, return_defaults=True)
    db_session.commit()
    return comments_edits_unique


def get_comment_id(identificator, comments_unique):
    for row in comments_unique:
        if row['identificator'] == identificator:
            return row['id']
# !!!! сюда ещё мб условие о проверки вложенности
    return None


def make_comment_id_dict(identificator, comments_unique):
    comment_id_dict ={}
    for row in comments_unique:
        if row['identificator'] == identificator:
            comment_id_dict[row['identificator']] = row['id']
            return row['id']
    return comment_id_dict


def load_data_to_models():
    mkdir_for_results(webapp.config_auth.FOLDER_NAME)
    logging.info('subreddit_data')
    subreddit_data = read_top_subreddit_csv('top_subreddits.csv')
    logging.info('comments_data')
    comments_data = read_comments_csv('comments.csv')
    comments_edits_data = read_comments_edits_csv('comments_edition.csv')

    os.chdir("..")  
    logging.info('top_subreddits')
    top_subreddits = save_top_subreddit(subreddit_data)
    logging.info('comments')
    comments = save_comments(comments_data, top_subreddits)
    comments_edits = save_comments_edits(comments_edits_data,top_subreddits)

if __name__ == '__main__':
    mkdir_for_results(webapp.config_auth.FOLDER_NAME)
 #  subreddit_data = read_top_subreddit_csv('top_subreddits.csv')
    subreddit_data = read_csv('top_subreddits.csv', webapp.config.fields_of_top_subreddit_csv)
#   comments_data = read_comments_csv('comments.csv')
    comments_data = read_csv('comments.csv', webapp.config.fields_of_comments_csv)
 #   comments_edits_data = read_comments_edits_csv('comments_edition.csv')
    comments_edits_data = read_csv('comments_edition.csv', webapp.config.fields_of_comments_edits_csv)
    os.chdir("..")  
    top_subreddits = save_top_subreddit(subreddit_data)
    comments = save_comments(comments_data, top_subreddits)
    comments_edits = save_comments_edits(comments_edits_data)