import csv
from webapp.db import db_session
import os
import time
import webapp.config_auth
from webapp.print_reddit_data import mkdir_for_results
from webapp.models import Top_subreddits, Comments



def read_top_subreddit_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['subreddit',  'author_subreddit', 'title', 'url_subreddit']
        reader = csv.DictReader(f, fields, delimiter=';')
        subreddit_data = []
        for row in reader:
            subreddit_data.append(row)
        return subreddit_data


def read_comments_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['identificator',  'author_comment', 'body', 'url_comment', 'nesting']
        reader = csv.DictReader(f, fields, delimiter=';')
        comments_data = []
        for row in reader:
            comments_data.append(row)
        return comments_data


def save_top_subreddit(all_data):
    processed = []
    top_subreddit_unique = []
    for row in all_data:
        if row['url_subreddit'] not in processed:
            top_subreddit = {'subreddit': row['subreddit'],'author_subreddit': row['author_subreddit'],
            'url_subreddit': row['url_subreddit'], 'title': row['title'], }
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
    for row in all_data:
        if row['identificator'] not in processed:
            comment = {'author_comment': row['author_comment'], 'body': row['body'], 'url_comment': row['url_comment'],
            'nesting': row['nesting'], 'identificator': row['identificator'],
              }
            comment['top_subreddit_id'] = get_top_subreddit_id(row['url_comment'], top_subreddit_unique)
            comments_unique.append(comment)
            processed.append(row['identificator'])
    db_session.bulk_insert_mappings(Comments, comments_unique, return_defaults=True)
    db_session.commit()
    return comments_unique


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
    subreddit_data = read_top_subreddit_csv('top_subreddits.csv')
    comments_data = read_comments_csv('comments.csv')
    os.chdir("..")  
    top_subreddits = save_top_subreddit(subreddit_data)
    comments = save_comments(comments_data, top_subreddits)

if __name__ == '__main__':
    mkdir_for_results(webapp.config_auth.FOLDER_NAME)
    subreddit_data = read_top_subreddit_csv('top_subreddits.csv')
    comments_data = read_comments_csv('comments.csv')
    os.chdir("..")  
    top_subreddits = save_top_subreddit(subreddit_data)
    comments = save_comments(comments_data, top_subreddits)