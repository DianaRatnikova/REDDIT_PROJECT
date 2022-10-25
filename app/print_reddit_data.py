import logging
import csv
import os
import app.config_auth

def mkdir_for_results(FOLDER_NAME):
    if not os.path.isdir(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)
    os.chdir(FOLDER_NAME)


# формирую строчку с данными поста
def get_top_subreddit_row(top_post, comment_url):
    top_post_info = {
                    'subreddit': top_post["data"]["subreddit"],
                    'author': top_post["data"]["author"],
                    'title': top_post["data"]["title"],
                    'url': comment_url
                    }
    subreddit_row = [top_post_info['subreddit'], top_post_info['author'],
                                 top_post_info['title'],top_post_info['url']]
    return subreddit_row


# записываем топ-посты в csv-файл построчно:
def write_top_subreddit_to_csv(result_subreddit, comments_url_list):
    mkdir_for_results(app.config_auth.FOLDER_NAME)
    with open('top_subreddits.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for (num_of_top_post, top_post) in enumerate(result_subreddit.json()["data"]["children"]):
            writer.writerow(get_top_subreddit_row(top_post, comments_url_list[num_of_top_post]))
    os.chdir("..")  


# формирую строчку с данными поста
def get_comment_row(top_post, comment_url):
    top_post_info = {
                    'subreddit': top_post["data"]["subreddit"],
                    'author': top_post["data"]["author"],
                    'title': top_post["data"]["title"],
                    'url': comment_url
                    }
    subreddit_row = [top_post_info['subreddit'], top_post_info['author'],
                                 top_post_info['title'],top_post_info['url']]
    return subreddit_row


def get_comment_row(comments, nesting_of_comment,comments_url):
    if "author" in comments and "body" in comments:
        comment_row = [comments['id'], comments['author'], comments['body'], comments_url, nesting_of_comment]

        edition_num = comments['edited']
        if not edition_num:
            edition_num = 0
        comments_edit_row = [comments['id'], comments['body'], int(edition_num),comments_url]
        
        mkdir_for_results(app.config_auth.FOLDER_NAME)
        with open('comments.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(comment_row)
        
        with open('comments_edition.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(comments_edit_row)    
        os.chdir("..")
        
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

