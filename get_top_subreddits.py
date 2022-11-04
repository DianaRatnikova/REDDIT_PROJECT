from app.authentication import get_reddit_auth_headers
import app.config_auth
from app.loader import load_data_to_models
from app.models import create_models
from app.reddit_requests import make_top_subreddit_requests, make_all_comments_request, construct_comments_url
from app.show_comments import show_comments
import logging
import os
from app.loader_renew import renew_subreddit, renew_comments

def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def delete_dir_with_old_results(FOLDER_NAME):
    if os.path.isdir(FOLDER_NAME):
        os.chdir(FOLDER_NAME)
        delete_file('comments_edition.csv')
        delete_file('top_subreddits.csv')
        delete_file('subreddits.csv')
        delete_file('edits_story.csv')
        delete_file('edits_story.txt')
        os.chdir("..")
        os.rmdir(FOLDER_NAME)


if __name__ == "__main__":
    logging.basicConfig(filename='loginfo.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    headers = get_reddit_auth_headers()
    delete_dir_with_old_results('result_data')

    menu = int(input("1 - загрузить новые данные в БД, \n2 - обновить изменения, \n3 - вывести актуальные комментарии \n"))
    
    if menu == 1:
        logging.info('<Loading new data to DB>')
        limit= int(input("Введите количество топ-новостей: "))
        logging.info('make_top_subreddit_requests(limit, headers):')
        result_subreddit = make_top_subreddit_requests(limit, headers)
        logging.info('make_all_comments_request(result_subreddit, headers)')
        make_all_comments_request(result_subreddit, headers)
        logging.info('construct_comments_url(result_subreddit)')
        comments_url_list = construct_comments_url(result_subreddit)
        logging.info('Creating database top_subreddits and comments')
        create_models()
        logging.info('Loader data to tables  top_subreddits and comments')
        load_data_to_models()
    elif menu == 2:
        logging.info('<Renewal>')
        print("Запрос на обновление")
        logging.info('Checking database: top_subreddits and comments')
        create_models()
        logging.info('Loader data to tables  top_subreddits and comments')
        logging.info('renew_subreddit')
        renew_subreddit(headers)
        logging.info('renew_comments')
        renew_comments(headers)
    else:
        logging.info('<Actual comments>')
        print("Актуальные комментарии")
        create_models()
        show_comments()