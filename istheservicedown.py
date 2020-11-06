'''
Collect comments from istheservicedown.com since 2020-03-01
'''

import json
import os
import time
from datetime import datetime

def get_current_start():
    with open("istheservicedown/config/start_time.json", "r") as fin:
        conf = json.load(fin)
    return conf["start_time"]

with open("istheservicedown/config/2019-12-30.json", "r") as fin:
    conf = json.load(fin)
    with open("istheservicedown/config/start_time.json", "w") as fout:
        json.dump(conf, fout)

curr_start = get_current_start()
while curr_start < 1599004800:  # 2020-05-01
    os.system('python3 disqus_list_posts.py -s istheservicedown/config/start_time.json -o istheservicedown -c istheservicedown/config/istheservicedown.json')
    print("Sleeping for 70 min to avoid Quota, starting from {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    time.sleep(60 * 70)
