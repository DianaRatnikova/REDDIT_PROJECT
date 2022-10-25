import app.config_auth
import requests
import logging

def get_reddit_auth_token():

    data = {'grant_type': 'password',
        'username': app.config_auth.user_name,
        'password': app.config_auth.password}

    logging.info("\n------------authentication details-----------")
    logging.info(f"{app.config_auth.user_name = }")
    logging.info(f"{app.config_auth.password = }")
# указываем параметры аутентификации
    auth = requests.auth.HTTPBasicAuth(app.config_auth.CLIENT_ID, app.config_auth.SECRET_TOKEN)
    result_post = requests.post(app.config_auth.URL_ACCESS_TOKEN,
                                auth=auth, data=data, headers=app.config_auth.HEADERS_INFO)
# convert response to JSON and pull access_token value
    TOKEN = result_post.json()['access_token']
    return TOKEN


def get_reddit_auth_headers():
    TOKEN = get_reddit_auth_token()

    logging.info(f"{app.config_auth.HEADERS_INFO = }")
    logging.info(f"{TOKEN = }")

    # add authorization to our headers dictionary
    headers =  app.config_auth.HEADERS_INFO | {'Authorization': f"bearer {TOKEN}"}
    logging.info(f"{headers = }")
    return headers
