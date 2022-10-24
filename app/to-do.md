в loaders:

def get_comment_id(identificator, comments_unique):
    for row in comments_unique:
        if row['identificator'] == identificator:
            return row['id']
# !!!! сюда ещё мб условие о проверки вложенности
    return None