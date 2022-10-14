import logging
import csv

# from webapp.reddit_requests import construct_comments_url

def show_all_comments(comments, nesting_of_comment, num_of_file):
    pass

# Не обязательно, потом удалить
def print_comments_url_list(result_subreddit):
    logging.info("-----Comments_URL---------")
    comments_url_list = construct_comments_url(result_subreddit)
    logging.info('\n'.join(comments_url_list))


# loop through each post retrieved from GET request
def show_subreddit_data(result_subreddit):    
    comments_url_list = construct_comments_url(result_subreddit)
  # logging.info(f"\n----TOP {LIMIT} news-------------------")
    logging.info(f"\n----TOP news-------------------")
#    show_subreddit_data(result_subreddit, comments_url_list)
    # запись в базу данных
   # pass
    return comments_url_list

# формирую строчку с данными поста
def get_top_subreddit_row(top_post, comment_url):
    top_post_info = {
                    'subreddit': top_post["data"]["subreddit"],
                    'author': top_post["data"]["author"],
                    'title': top_post["data"]["title"],
                    'url': comment_url
                    }
    subreddit_row = [top_post_info['subreddit'], top_post_info['author'],
                                 top_post_info['title'],top_post_info['url'],]
    return subreddit_row

# записываем топ-посты в csv-файл построчно:
def write_top_subreddit_to_csv(result_subreddit, comments_url_list):
    with open('top_subreddits.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for (num_of_top_post, top_post) in enumerate(result_subreddit.json()["data"]["children"]):
            writer.writerow(get_top_subreddit_row(top_post, comments_url_list[num_of_top_post]))


# формирую строчку с данными поста
def get_comment_row(top_post, comment_url):
    top_post_info = {
                    'subreddit': top_post["data"]["subreddit"],
                    'author': top_post["data"]["author"],
                    'title': top_post["data"]["title"],
                    'url': comment_url
                    }
    subreddit_row = [top_post_info['subreddit'], top_post_info['author'],
                                 top_post_info['title'],top_post_info['url'],]
    return subreddit_row


def get_comment_row(comments, nesting_of_comment,comments_url):
    if "author" in comments and "body" in comments:
        comment_row = [comments['author'], comments['body'], comments_url, nesting_of_comment]
        with open('comments.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(comment_row)  
        author = comments['author']

    if 'replies' in comments:
        if comments['replies'] == '':
            nesting_of_comment -= 1
        else:
            for comments_dict in comments['replies']['data']['children']:
                if comments_dict['kind'] != "more":
                    nesting_of_comment += 1
                    get_comment_row(comments_dict['data'], nesting_of_comment, comments_url)
                else:
                    pass
                nesting_of_comment -= 1


# записываем топ-посты в csv-файл построчно:
def write_comments_to_csv(result_subreddit, comments_url_list):
    with open('top_subreddits.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for (num_of_top_post, top_post) in enumerate(result_subreddit.json()["data"]["children"]):
            writer.writerow(comment_row)