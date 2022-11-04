from sqlalchemy import true
import app.config_auth
from app.print_reddit_data import get_comment_row, get_one_subreddit_row, write_one_subreddit_to_csv
import logging
import requests


def construct_comments_url(result_subreddit: any) -> list:
    comments_url_list = []
    for post in result_subreddit.json()["data"]["children"]:
        comments_url = app.config_auth.CONST_URL + post['data']['permalink']
        comments_url = comments_url[:-1]+'.json?sort=new'  # сформирована ссылка на комменты
        comments_url_list.append(comments_url)
    return comments_url_list


def make_top_subreddit_requests(limit, headers):
# формирую словарь result_subreddit.json()
    result_subreddit = requests.get(f'https://oauth.reddit.com/top.json?limit={limit}', headers=headers)
    logging.info("\n------------request for top subreddits was done-----------")
    logging.info(f'{result_subreddit.status_code =}')
    return result_subreddit


# разбор странички с постом
def make_one_subreddit_request(comment_url, num_of_file, headers):
    result_comments = requests.get(f'{comment_url}', headers=headers)
    # нулевой элемент списка содержит инфу о посте, первый - все комменты
    one_subreddit_json = result_comments.json()[0]['data']['children']
    logging.info(f'Number of comments for post {num_of_file+1}: {len(one_subreddit_json)}')
    return one_subreddit_json

# разбор странички с комментариями
def make_one_comment_request(comment_url, num_of_file, headers):
    result_comments = requests.get(f'{comment_url}', headers=headers)
    # нулевой элемент списка содержит инфу о посте, первый - все комменты
    comment_json = result_comments.json()[1]['data']['children']
    logging.info(f'Number of comments for post {num_of_file+1}: {len(comment_json)}')
    return comment_json

def write_comments_to_csv(comments_url, comment_json: list):
    comment_edits_list = []
    if comment_json is not None:
        for comment_for_top_post in comment_json:
            comments_edit_row = get_comment_row(comment_for_top_post['data'], 0, comments_url)
            comment_edits_list.append(comments_edit_row)
    return comment_edits_list

def make_all_comments_request(result_subreddit, headers):
    comments_url_list = construct_comments_url(result_subreddit)
    for (num_of_file, comment_url) in enumerate(comments_url_list):
        comment_json = make_one_comment_request(comment_url, num_of_file, headers)
        one_subreddit_json = make_one_subreddit_request(comment_url, num_of_file, headers)
        write_comments_to_csv(comment_url, comment_json)
        write_one_subreddit_to_csv(comment_url, one_subreddit_json)