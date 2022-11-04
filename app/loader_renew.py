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
    urls = [url_addr[0] for url_addr in query_url]
    return urls

def get_edit_nums_from_db(url):
    query_num_edit = db_session.query(Subreddit.edition_num).filter(Subreddit.url_subreddit == url) 
    num_edit_list = [num_edit[0] for num_edit in query_num_edit]
    return num_edit_list


def renew_comments(headers):
    new_comments_unique = []
    new_comment = {}
    comments_edits_data = []
# вытащить url-адреса комментов     
    urls = get_subreddit_urls_from_db()

    for url in urls:
        # получаю актуальную версию json для поста из бд.
        comments_json = make_one_comment_request(url, 0, headers)
        if comments_json is not None:
        # записываем коменты в csv-файл построчно:
            comment_edits_list = write_comments_to_csv(url, comments_json)
            for one_edit in comment_edits_list:
                if one_edit is not None:
                    one_edit_dict = {
                                    'identificator': one_edit[0],
                                    'author_comment':one_edit[1],
                                    'body': one_edit[2],
                                    'edition_num': one_edit[3],
                                    'url_comment': one_edit[4],
                                    'nesting': one_edit[5],
                                }
                    comments_edits_data.append(one_edit_dict)

    logging.info(f'{comment_edits_list = }')
    logging.info('Reading csv files...')
    logging.info('End reading')  
    logging.info('save_comments')  
    comments = save_comments(comments_edits_data)
    logging.info('End save_comments')  



def make_top_subreddit_dict(subreddit_row):
    top_subreddit = {'subreddit': subreddit_row[0],
                     'author_subreddit': subreddit_row[1],
                     'title': subreddit_row[2], 
                     'url_subreddit': subreddit_row[3], 
                     'edition_num': subreddit_row[4]
                   }
    return top_subreddit


def renew_subreddit(headers):
    new_subreddit_unique = []
    top_subreddit = {}

# вытащить url-адреса постов      
    urls = get_subreddit_urls_from_db()
    print("renew_subreddit: urls = ", '\n'.join(urls))

    for url in urls:
        # получаю актуальную версию json для поста из бд.
        one_subreddit_json = make_one_subreddit_request(url, 0, headers)

        if one_subreddit_json is not None:
            for one_subreddit in one_subreddit_json:
                subreddit_row = get_one_subreddit_row(one_subreddit, url)

            top_subreddit = make_top_subreddit_dict(subreddit_row)
            num_edit_list = get_edit_nums_from_db(url)

            logging.info(f"{subreddit_row[4] = }")    
            logging.info(f"{num_edit_list = }") 
 # если номера редакции нет в списке           
            if subreddit_row[4] not in num_edit_list:
                new_subreddit_unique.append(top_subreddit)
            logging.info(f"{new_subreddit_unique = }")

    db_session.bulk_insert_mappings(Subreddit, new_subreddit_unique, return_defaults=True)
    db_session.commit()
    return new_subreddit_unique