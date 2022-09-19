import gzip
import json


def seperate_str_dict(data):
    dict_list = []
    null = None
    false = False
    true = True
    raw_list = data.split('\n')

    for i in range(1,len(raw_list)):
        raw = raw_list[i]
        if len(raw) < 1:
            continue
        dict_each = eval(raw)
        dict_list.append(dict_each)
    
    return dict_list

def filter_rule_1():
    pass

def filter_rule_2(user_name,tweet_text):
    '''
    User identity: Black, Hispanic, Asian American, etc
    Topic: ob/GYN, pregnancy, doctor
    '''
    User_keywords = ['black', 'hispanic','asian american']
    Topic_keywords = ['ob/gyn','pregnancy','doctor']

    for kword in User_keywords:
        if kword in user_name:
            return True

    for kword in Topic_keywords:
        if kword in tweet_text:
            return True

    return False

def filter_rule_3(hash_tag_list,tweet_text):
    Hash_keywords = ['#BMMA'.lower()]
    # for i in range(len(hash_tag_list)):
    #     hash_tag_list[i] = hash_tag_list[i].lower()

    for kword in Hash_keywords:
        if kword in tweet_text:
            return True
        # if kword in hash_tag_list:
        #     return True
    
    return False

def filter_rule_4(tweet_text):
    if '@blkmamasmatter' in tweet_text:
        return True
    
    return False

def filter_sample(dict_each):
    '''
    1). user profile + topic keyword
    2). User identify keywords + topic keyword
    3). Hashtag #BMMA
    4). User handle @blkmamasmatter
    '''
    user_name = ''
    if len(dict_each["entities"]["user_mentions"]) > 0:
        user_name = dict_each["entities"]["user_mentions"][0]["screen_name"] 
    tweet_text = (dict_each["text"].lower())

    # Rule 1
    # Have no profile
    flag_1 = False

    # Rule 2
    flag_2 = filter_rule_2(user_name,tweet_text)

    # Rule 3
    hash_tag_list = dict_each["entities"]["hashtags"]
    flag_3 = filter_rule_3(hash_tag_list,tweet_text)

    # Rule 4
    flag_4 = filter_rule_4(tweet_text)

    # Combine
    return flag_1 or flag_2 or flag_3 or flag_4


def filter_dict_list(dict_list):
    selected_list = []
    for dict_each in dict_list:
        if filter_sample(dict_each):
            # Selected
            selected_list.append(dict_each)
    return selected_list


def main_process():

    with gzip.open("2020_12_31_00.json.gz", "r") as f:
        data = f.read()

    data = data.decode()
    dict_list = seperate_str_dict(data)
    selected_list = filter_dict_list(dict_list)
    
    with open('example_found.txt','a') as f:
        for dict_each in selected_list:
            tweet_test = dict_each["text"]
            for char in tweet_test:
                try:
                    f.write(char)
                except:
                    continue
            f.write('\n')
        # print(tweet_test)
        # with open('example_found.txt','w') as f:
        #     f.write(tweet_test+'\n')

    pass






if __name__ == '__main__':
    main_process()