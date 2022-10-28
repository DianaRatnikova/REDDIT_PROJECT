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

from app.reddit_requests import make_one_subreddit_request, write_comments_to_csv, make_one_comment_request
from app.print_reddit_data import get_one_subreddit_row
from app.loader import read_csv, save_comments


def get_subreddit_urls_from_db():
    query_url = db_session.query(Subreddit.url_subreddit).distinct()
    urls = []
    for url_addr in query_url:
        urls.append(url_addr[0])
    return urls


def renew_subreddit(headers):
    processed = []
    new_subreddit_unique = []
    top_subreddit = {}

# вытащить url-адреса постов      
    query_url = db_session.query(Subreddit.url_subreddit).distinct()
    urls = get_subreddit_urls_from_db()
    
    logging.info("renew_subreddit: urls = ", '\n'.join(urls))

    for url in urls:
        # получаю актуальную версию json для поста из бд.
        one_subreddit_json = make_one_subreddit_request(url, 0, headers)

        if one_subreddit_json is not None:
# записываем топ-посты в csv-файл построчно:
# def write_one_subreddit_to_csv(comments_url, one_subreddit_json: list):
            for one_subreddit in one_subreddit_json:
                subreddit_row = get_one_subreddit_row(one_subreddit['data'], url)
            print(f"{subreddit_row = }")

            subreddit_loaded = 0 # 'False'
 #           if subreddit_row['url_subreddit'] not in processed:
            top_subreddit = {'subreddit': subreddit_row[0],
                            'author_subreddit': subreddit_row[1],
                            'title': subreddit_row[2], 
                            'url_subreddit': subreddit_row[3], 
                            'edition_num': subreddit_row[4]
                            }
#            processed.append(top_subreddit['url_subreddit'])
            subreddit_loaded = 0  #'False'

            query_num_edit = db_session.query(Subreddit.edition_num).filter(Subreddit.url_subreddit == url)   #.distinct()
            num_edit_list = []
            for num_edit in query_num_edit:
	            num_edit_list.append(num_edit[0])
            logging.info(f"{subreddit_row[4] = }")    
            logging.info(f"{num_edit_list = }") 
            if subreddit_row[4] not in num_edit_list:
                subreddit_loaded = 1 #'True'
                new_subreddit_unique.append(top_subreddit)
            logging.info(f"{new_subreddit_unique = }")
# return_defaults=True говорит bulk_insert_mappings, 
# что когда база присвоит компаниям id, их нужно добавить в top_subreddit_unique.
    db_session.bulk_insert_mappings(Subreddit, new_subreddit_unique, return_defaults=True)
    db_session.commit()
    return new_subreddit_unique
 

def renew_comments(headers):
    processed = []
    new_comments_unique = []
    new_comment = {}

# вытащить url-адреса комментов     
    query_url = db_session.query(Comment.url_comment).distinct()
    urls = get_subreddit_urls_from_db()

    for url in urls:
        # получаю актуальную версию json для поста из бд.
        comments_json = make_one_comment_request(url, 0, headers)
        if comments_json is not None:
        # записываем коменты в csv-файл построчно:
            write_comments_to_csv(url, comments_json)
   
    logging.info('Reading csv files...')
    mkdir_for_results(app.config_auth.FOLDER_NAME)
    comments_edits_data = read_csv(app.config.filename_comments_edition, app.config.fields_of_comments_edits_csv)
    os.chdir("..")
    logging.info('End reading')  
    logging.info('save_comments')  
    comments = save_comments(comments_edits_data)
    logging.info('End save_comments')  