CLIENT_ID = 'OIv-IBW8oFWUbaTrmT4TjA'
SECRETE_KEY = 'PNR6CB7MWgMfuKGGLhh1qgdzA5zxdg'

import requests
import time
import csv
import re
import os.path as osp

auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRETE_KEY)

data = {
    'grant_type':'password',
    'username':'ming_666',
    'password':'MingsPW4reddit..'
}
headers = {'User-Agent':'Ming/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                   auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'
requests.get('https://oauth.reddit.com/api/v1/me',headers=headers)

ONCE_NUM = 1
WEB_LINK = "https://oauth.reddit.com/r/IVF/new"
COMMENT_PRE = "https://oauth.reddit.com/"

def get_main_post(data_in):
    title = data_in['data']['title']
    author = data_in['data']['author']
    created_time_i = data_in['data']['created']
    created_time_i = int(created_time_i) 
    created_time_i = time.localtime(created_time_i)
    created = time.strftime("%m/%d/%Y %H:%M", created_time_i) 
    ups = data_in['data']['ups']
    num_comments = data_in['data']['num_comments']
    name = data_in['data']['name']
    url = data_in['data']['url']
    permalink = data_in['data']['permalink']
    comment_link = COMMENT_PRE + permalink.strip('/') + '.json'
    selftext = data_in['data']['selftext']
    return title, author, created, ups, num_comments, name, url, comment_link, selftext


def get_comment(data_comment):
    author = data_comment['data']['author']
    body = data_comment['data']['body']
    created_time_i = data_comment['data']['created']
    created_time_i = int(created_time_i) 
    created_time_i = time.localtime(created_time_i)
    created = time.strftime("%m/%d/%Y %H:%M", created_time_i) 
    replies = data_comment['data']['replies']
    name = data_comment['data']['name']
    return author,body,created,replies,name
    pass

def once_main(main_article_name,all_count_now,writer):
    once_str = '\'' + str(ONCE_NUM) + '\''
    res = requests.get(WEB_LINK,
                   headers=headers,params={'limit':once_str,'after':main_article_name})
    for i in range(ONCE_NUM):
        post_id = all_count_now + i + 1
        data_in = res.json()['data']['children'][i]
        title_p, author_p, created_p, ups_p, num_comments_p, main_article_name, url, comment_link, selftext_p = get_main_post(data_in)
        selftext_p = selftext_p.replace('\n','\\')
        print()
        print('===========Main Artucle===========:')
        print(title_p,author_p)
        print(selftext_p.replace('\n','\\'))
        content = [author_p,created_p,num_comments_p,ups_p,selftext_p,'','','','','',main_article_name]
        writer.writerow(content)
        
        
        res_comment_layer1 = requests.get(comment_link,headers=headers,params={'showmore':True})
        comment_layer1_len = len(res_comment_layer1.json()[1]['data']['children'])
        # print(comment_layer1_len)
        
        for j in range(comment_layer1_len):
            # data_comment = res_comment_layer1.json()[1]['data']['children']
            data_comment = res_comment_layer1.json()[1]['data']['children'][j]
            author,body,created,replies,name = get_comment(data_comment)
            body = body.replace('\n','\\')
            print('---------------Comment Layer 1:')
            print(body.replace('\n','\\'),author)
            content = [author_p,created_p,num_comments_p,ups_p,selftext_p,body,author,created,'1',str(post_id),main_article_name]
            writer.writerow(content)

            
            if replies != '':
                layer_2 = replies['data']['children']
                comment_layer2_len = len(layer_2)
                for k in range(comment_layer2_len):
                    data_comment_l2 = layer_2[k]
                    author,body,created,replies,name = get_comment(data_comment_l2)
                    body = body.replace('\n','\\')
                    print('---------------Comment Layer 2:')
                    print(body.replace('\n','\\'),author)
                    content = [author_p,created_p,num_comments_p,ups_p,selftext_p,body,author,created,'2',str(post_id),main_article_name]
                    writer.writerow(content)


                    if replies != '':
                        layer_3 = replies['data']['children']
                        comment_layer3_len = len(layer_3)
                        for l in range(comment_layer3_len):
                            data_comment_l3 = layer_3[l]
                            author,body,created,replies,name = get_comment(data_comment_l3)
                            body = body.replace('\n','\\')
                            # body = re.sub('[\u0000-\uffff]+','',body)
                            print('---------------Comment Layer 3:')
                            print(body.replace('\n','\\'),author)
                            content = [author_p,created_p,num_comments_p,ups_p,selftext_p,body,author,created,'3',str(post_id),main_article_name]
                            writer.writerow(content)

    return main_article_name


if __name__ == '__main__':
    all_num = 2
    all_count = 0
    file_count = 1
    main_article_name = ''
    
    main_file_path = 'IVF_post'
    
    fileHeader = []
    fileHeader = ['username','datetime','replies_counts','favorites_counts','text','reply_content',\
                'reply_username','reply_datetime','reply_level','corresponding_post', 'post_id']
    

    while all_count < all_num:
        if all_count % 1000 == 0:
            real_f_p = osp.join(main_file_path,str(file_count)+'.csv')
            csvFile = open(real_f_p, "a", encoding="utf-8", newline='')
            writer = csv.writer(csvFile)
            writer.writerow(fileHeader)
        main_article_name = once_main(main_article_name,all_count,writer)
        all_count += ONCE_NUM

    csvFile.close()
pass
    
    