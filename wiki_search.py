import wikipedia


def search_some_info(info):
    wikipedia.set_lang('ru')
    print('I am searching')
    all_res = wikipedia.search(info, results=5)
    if len(all_res) == 0:
        return False
    result = wikipedia.summary(all_res[0], 3)
    return result
