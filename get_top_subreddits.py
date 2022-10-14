from webapp.authentication import get_headers
from webapp.reddit_requests import make_top_subreddit_requests, make_all_comments_request, construct_comments_url
from webapp.print_reddit_data import write_top_subreddit_to_csv


import logging

if __name__ == "__main__":
    logging.basicConfig(filename='loginfo.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    headers = get_headers()

    LIMIT = int(input("Введите количество топ-новостей: "))
    result_subreddit = make_top_subreddit_requests(LIMIT, headers)
    make_all_comments_request(result_subreddit, headers)
    comments_url_list = construct_comments_url(result_subreddit)
    write_top_subreddit_to_csv(result_subreddit, comments_url_list)