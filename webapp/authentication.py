import webapp.config_auth
import requests
import logging

def get_reddit_auth_token():

    data = {'grant_type': 'password',
        'username': webapp.config_auth.user_name,
        'password': webapp.config_auth.password}

    logging.info("\n------------authentication details-----------")
    logging.info(f"{webapp.config_auth.user_name = }")
    logging.info(f"{webapp.config_auth.password = }")
# указываем параметры аутентификации
    auth = requests.auth.HTTPBasicAuth(webapp.config_auth.CLIENT_ID, webapp.config_auth.SECRET_TOKEN)
    result_post = requests.post(webapp.config_auth.URL_ACCESS_TOKEN,
                                auth=auth, data=data, headers=webapp.config_auth.HEADERS_INFO)
# convert response to JSON and pull access_token value
    TOKEN = result_post.json()['access_token']
    return TOKEN


def get_reddit_auth_headers():
    TOKEN = get_reddit_auth_token()

    logging.info(f"{webapp.config_auth.HEADERS_INFO = }")
    logging.info(f"{TOKEN = }")

    # add authorization to our headers dictionary
    headers =  webapp.config_auth.HEADERS_INFO | {'Authorization': f"bearer {TOKEN}"}
    logging.info(f"{headers = }")
    return headers
