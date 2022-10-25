from app.authentication import get_reddit_auth_headers
import app.config_auth
from app.loader import load_data_to_models
from app.models import create_models
from app.print_reddit_data import write_top_subreddit_to_csv
from app.reddit_requests import make_top_subreddit_requests, make_all_comments_request, construct_comments_url
import logging
import os


def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def delete_dir_with_old_results(FOLDER_NAME):
    if os.path.isdir(FOLDER_NAME):
        os.chdir(FOLDER_NAME)
        delete_file('comments.csv')
        delete_file('comments_edition.csv')
        delete_file('top_subreddits.csv')
        os.chdir("..")
        os.rmdir(FOLDER_NAME)



if __name__ == "__main__":
    logging.basicConfig(filename='loginfo.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    headers = get_reddit_auth_headers()
    delete_dir_with_old_results('result_data')
    limit= int(input("Введите количество топ-новостей: "))
    logging.info('make_top_subreddit_requests(limit, headers):')
    result_subreddit = make_top_subreddit_requests(limit, headers)
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