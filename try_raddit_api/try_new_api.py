import requests

# query="seo" #Define Your Query
# url = f"https://api.pushshift.io/reddit/search/comment/?q={query}"
# request = requests.get(url)
# json_response = request.json()
# json_response

def get_pushshift_data(data_type, **kwargs):
    """
    Gets data from the pushshift api.
 
    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.
 
    Read more: https://github.com/pushshift/api
    """
 
    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()



data_type="submission"     # give me comments, use "submission" to publish something
# query="python"          # Add your query
# duration="30d"          # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
size=2                  # maximum 1000 comments
# sort_type="score"       # Sort by score (Accepted: "score", "num_comments", "created_utc")
sort="desc"             # sort descending
aggs="link_id"        #"author", "link_id", "created_utc", "subreddit"
subreddit = 'ivf'
before = 1641589092



data = get_pushshift_data(data_type=data_type,                
                   before=before,          
                   size=size,
                   sort=sort,
                   subreddit=subreddit)


def get_pushshift_data_2(): 
    url = f"https://api.pushshift.io/reddit/search/submission/?after=1641509064&aggs=link_id&size=2&subreddit=ivf"
    request = requests.get(url)
    return request.json()

data = get_pushshift_data_2()

pass

# data = data.get("aggs").get(aggs)

import pandas as pd
df = pd.DataFrame.from_records(data)[0:10]
df

# Call the API
data = get_pushshift_data(data_type=data_type,
                          q=query,
                          after="7d",
                          size=10,
                          sort_type=sort_type,
                          sort=sort).get("data")
 
# Select the columns you care about
df = pd.DataFrame.from_records(data)[["author", "subreddit", "score", "body", "permalink"]]
 
# Keep the first 400 characters
df['body'] = df['body'].str[0:400] + "..."
 
# Append the string to all the permalink entries so that we have a link to the comment
df['permalink'] = "https://reddit.com" + df['permalink'].astype(str)
 
 
# Create a function to make the link to be clickable and style the last column
def make_clickable(val):
    """ Makes a pandas column clickable by wrapping it in some html.
    """
    return '<a href="{}">Link</a>'.format(val,val)
 
 
df.style.format({'permalink': make_clickable})

pass