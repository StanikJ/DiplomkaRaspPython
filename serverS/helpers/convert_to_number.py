def convert_to_number(word:str):
    if word == 'Zapnut':
        return 1
    elif word == 'Vypnut':
        return 0
    else:
        return int(word)