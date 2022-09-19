CLIENT_ID = 'OIv-IBW8oFWUbaTrmT4TjA'
SECRETE_KEY = 'PNR6CB7MWgMfuKGGLhh1qgdzA5zxdg'

import requests
import time
import csv
import re
import os.path as osp

auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRETE_KEY)

data_user = {
    'grant_type':'password',
    'username':'ming_666',
    'password':'MingsPW4reddit..'
}
headers = {'User-Agent':'Ming/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                   auth=auth, data=data_user, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'
requests.get('https://oauth.reddit.com/api/v1/me',headers=headers)


def get_main_post(data_in,comment_pre):
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
    comment_link = comment_pre + permalink.strip('/') + '.json'
    selftext = data_in['data']['selftext']
    return title, author, created, ups, num_comments, name, url, comment_link, selftext

def get_main_post_2(data_in,comment_pre):
    title = data_in['title']
    author = data_in['author']
    created_time_i = data_in['created_utc']
    url = data_in['url']
    permalink = data_in['permalink']
    comment_link = comment_pre + permalink.strip('/') + '.json'
    selftext = data_in['selftext']
    return title, author, created_time_i, url, comment_link, selftext

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

def get_pushshift_data(data_type, **kwargs):
    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()

def once_main(started_search_time,all_count,writer,once_num,comment_pre,subreddit_needed):
    data_type="submission"     # give me comments, use "submission" to publish something
    size=once_num              # maximum 1000 comments
    sort="desc"             # sort descending
    subreddit = subreddit_needed
    before = started_search_time
    
    data_all_post = get_pushshift_data(data_type=data_type,                
                   before=before,          
                   size=size,
                   sort=sort,
                   subreddit=subreddit)
    
    data_all_post = data_all_post['data']    
    for i in range(len(data_all_post)):
        post_id = all_count + i + 1
        data_in = data_all_post[i]
        
        # title_p, author_p, created_p, ups_p, num_comments_p, main_article_name, url, comment_link, selftext_p = get_main_post(data_in)
        _, _, created_time_stamp, url, comment_link, _ = get_main_post_2(data_in,comment_pre)
        
        try:
            res_comment_layer1 = requests.get(comment_link,headers=headers,params={'showmore':True})
        except:
            print('Raise Exception')
            continue
        data_single_post = res_comment_layer1.json()[0]['data']['children'][0]
        title_p, author_p, created_p, ups_p, num_comments_p, main_article_name, url, comment_link, selftext_p = \
                                        get_main_post(data_single_post,comment_pre)
        selftext_p = selftext_p.replace('\n','')
                                        
        # print()
        # print('===========Main Artucle===========:')
        # print(title_p,author_p)
        # print(selftext_p.replace('\n',''))
        
        # print(comment_layer1_len)
        content = [author_p,created_p,num_comments_p,ups_p,selftext_p,'','','','','',main_article_name]
        writer.writerow(content)
        
        comment_layer1_len = len(res_comment_layer1.json()[1]['data']['children'])
        for j in range(comment_layer1_len):
            # data_comment = res_comment_layer1.json()[1]['data']['children']
            data_comment = res_comment_layer1.json()[1]['data']['children'][j]
            try:
                author,body,created,replies,name = get_comment(data_comment)
            except:
                continue
            body = body.replace('\n','')
            # print('---------------Comment Layer 1:')
            # print(body.replace('\n',''),author)
            content = [author_p,created_p,num_comments_p,ups_p,selftext_p,body,author,created,'1',str(post_id),main_article_name]
            writer.writerow(content)

            
            if replies != '':
                layer_2 = replies['data']['children']
                comment_layer2_len = len(layer_2)
                for k in range(comment_layer2_len):
                    data_comment_l2 = layer_2[k]
                    try:
                        author,body,created,replies,name = get_comment(data_comment_l2)
                    except:
                        continue
                    body = body.replace('\n','')
                    # print('---------------Comment Layer 2:')
                    # print(body.replace('\n',''),author)
                    content = [author_p,created_p,num_comments_p,ups_p,selftext_p,body,author,created,'2',str(post_id),main_article_name]
                    writer.writerow(content)


                    if replies != '':
                        layer_3 = replies['data']['children']
                        comment_layer3_len = len(layer_3)
                        for l in range(comment_layer3_len):
                            data_comment_l3 = layer_3[l]
                            try:
                                author,body,created,replies,name = get_comment(data_comment_l3)
                            except:
                                continue
                            body = body.replace('\n','')
                            # body = re.sub('[\u0000-\uffff]+','',body)
                            # print('---------------Comment Layer 3:')
                            # print(body.replace('\n',''),author)
                            content = [author_p,created_p,num_comments_p,ups_p,selftext_p,body,author,created,'3',str(post_id),main_article_name]
                            writer.writerow(content)
                            
        pass

    return created_time_stamp


if __name__ == '__main__':
    
    once_num = 20
    file_split_num = 20
    comment_pre = "https://oauth.reddit.com/"
    
    all_count = 0
    file_count = 1
    started_search_time = 1641016800
    # 2022-01-01
    # end_time = 1577858400
    # 2020-01-01
    end_time = 1640757600
    
    save_file_path = 'sample_post'
    fileHeader = []
    fileHeader = ['username','datetime','replies_counts','favorites_counts','text','reply_content',\
                'reply_username','reply_datetime','reply_level','corresponding_post', 'post_id']
    
    subreddit_needed = 'ivf'

    while started_search_time > end_time:
        s = time.time()
        if all_count % file_split_num == 0:
            real_f_p = osp.join(save_file_path,str(file_count)+'.csv')
            csvFile = open(real_f_p, "a", encoding="utf-8", newline='')
            writer = csv.writer(csvFile)
            writer.writerow(fileHeader)
            file_count += 1
        started_search_time = once_main(started_search_time,all_count,writer,once_num,comment_pre,subreddit_needed)
        created_time_i = int(started_search_time) 
        created_time_i = time.localtime(created_time_i)
        created_time_i = time.strftime("%m/%d/%Y %H:%M", created_time_i) 
        all_count += once_num
        print('Finished:',all_count,'\tDate:',created_time_i,'\tTime Used:',(time.time()-s)/60,'(min)')

    csvFile.close()
pass
    
    