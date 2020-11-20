import argparse
import requests
import pickle
import json
import datetime
import time


def main(config_file):
    with open(config_file, "r") as fin:
        config = json.load(fin)

    joint_response = list()

    url = "https://disqus.com/api/3.0/forums/listThreads.json"
    forum_name = config["forum_name"]
    api_key = config["api_key"]

    cursor = None
    done = False
    num_requests = 0
    while not done:

        limit = 100
        order = "asc"

        try:
            if cursor is None:
                response = requests.get("{}?forum={}&api_key={}&limit={}&order={}".format(
                    url,
                    forum_name,
                    api_key,
                    limit,
                    order
                ))
            else:
                response = requests.get("{}?forum={}&api_key={}&limit={}&order={}&cursor={}".format(
                    url,
                    forum_name,
                    api_key,
                    limit,
                    order,
                    cursor
                ))
            response_json = response.json()
            joint_response += response_json["response"]
            if response_json["cursor"]["hasNext"]:
                cursor = response_json["cursor"]["next"]
            else:
                print('done!')
                done = True

            num_requests += 1

            if num_requests % 10 == 0:
                print("Fetched from {} to {}".format(
                    response_json["response"][0]['createdAt'], response_json["response"][-1]['createdAt']
                ))

            if num_requests % 150 == 0:
                if not done:
                    print("Sleeping for 70 min starting from {}".format(
                        datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                    time.sleep(60*70)

        except:

            print('request failed! perhaps due to quota exceeded')
            print("Sleeping for 70 min starting from {}".format(
                datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            time.sleep(60 * 70)


    with open(config['output'], 'wb') as fout:
        pickle.dump(joint_response, fout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=True)
    args = parser.parse_args()
    main(config_file=args.config)
