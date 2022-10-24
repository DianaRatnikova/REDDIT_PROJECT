import logging
import requests
import webapp.config_auth

# from webapp.authentication import get_reddit_auth_headers
from webapp.print_reddit_data import get_comment_row

def construct_comments_url(result_subreddit: any) -> list:
    comments_url_list = []
    for post in result_subreddit.json()["data"]["children"]:
        comments_url = webapp.config_auth.CONST_URL + post['data']['permalink']
        comments_url = comments_url[:-1]+'.json'  # сформирована ссылка на комменты
        comments_url_list.append(comments_url)
    return comments_url_list


# вытащить топовые посты
def make_top_subreddit_requests(limit, headers):
# формирую словарь result_subreddit.json()
    result_subreddit = requests.get(f'https://oauth.reddit.com/top.json?limit={limit}', headers=headers)

    logging.info("\n------------request for top subreddits was done-----------")
    logging.info(f'{result_subreddit.status_code =}')

  #  print_comments_url_list(result_subreddit) # Не обязательно, потом удалить
    return result_subreddit


# разбор странички с комментариями
def make_one_comment_request(comments_url, num_of_file, headers):
    result_comments = requests.get(f'{comments_url}', headers=headers)
    # нулевой элемент списка содержит инфу о посте, первый - все комменты
    comment_json = result_comments.json()[1]['data']['children']
    logging.info(f'Number of comments for post {num_of_file+1}: {len(comment_json)}')

    for comment_for_top_post in comment_json:
        get_comment_row(comment_for_top_post['data'], 0, comments_url)
     
        pass


def make_all_comments_request(result_subreddit, headers):
    comments_url_list = construct_comments_url(result_subreddit)
    for (num_of_file, comment_url) in enumerate(comments_url_list):
        make_one_comment_request(comment_url, num_of_file, headers)