from webapp.authentication import get_headers
from webapp.reddit_requests import make_top_subreddit_requests, make_all_comments_request, construct_comments_url
from webapp.print_reddit_data import write_top_subreddit_to_csv
from webapp.loader import load_data_to_models
from webapp.models import create_models

import logging

if __name__ == "__main__":
    logging.basicConfig(filename='loginfo.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    headers = get_headers()

    LIMIT = int(input("Введите количество топ-новостей: "))
    logging.info('make_top_subreddit_requests(LIMIT, headers):')
    result_subreddit = make_top_subreddit_requests(LIMIT, headers)
    logging.info('make_all_comments_request(result_subreddit, headers)')
    make_all_comments_request(result_subreddit, headers)
    logging.info('construct_comments_url(result_subreddit)')
    comments_url_list = construct_comments_url(result_subreddit)
    logging.info('write_top_subreddit_to_csv(result_subreddit, comments_url_list)')
    write_top_subreddit_to_csv(result_subreddit, comments_url_list)
    
    logging.info('Creating database top_subreddits and comments')
    create_models()
    logging.info('Loader data to tables  top_subreddits and comments')
    load_data_to_models()