def checkbox_to_db_value(word):
    if word == 'on':
        return 1
    elif word == None:
        return 0
    else:
        return int(word)