import argparse
import requests
import os
import json
import tqdm
import datetime


def datetime2timestamp(datetime_str):
    tokens = datetime_str.split("T")
    year, month, day = tuple(map(int, tokens[0].split("-")))
    hr, minute, sec = tuple(map(int, tokens[1].split(":")))
    return datetime.datetime(year, month, day, hr, minute, sec).timestamp()


def main(start_time_file, output_dir, config_file):
    with open(config_file, "r") as fin:
        config = json.load(fin)

    with open(start_time_file, "r") as fin:
        start_time = json.load(fin)["start_time"]

    file_name = os.path.join(output_dir, str(start_time) + ".tsv")

    fout = open(file_name, "w")
    fout.write('id\tcreatedAt\tusername\tforum\traw_message\n')

    since = start_time
    url = "https://disqus.com/api/3.0/forums/listPosts.json"
    forum_name = config["forum_name"]
    api_key = config["api_key"]

    for _ in tqdm.tqdm(range(60)):

        limit = 100
        order = "asc"

        response = requests.get("{}?forum={}&api_key={}&limit={}&order={}&since={}".format(
            url,
            forum_name,
            api_key,
            limit,
            order,
            int(since)
        ))
        response_json = response.json()

        for resp in response_json["response"]:
            fout.write("{}\t{}\t{}\t{}\t{}\n".format(
                resp["id"], resp["createdAt"], resp["author"].get("username", None), resp["forum"],
                resp["raw_message"].strip().replace("\n", "")
            ))

        since = int(datetime2timestamp(response_json["response"][-1]["createdAt"])) + 1

    fout.close()

    start_datetime = datetime.datetime.fromtimestamp(start_time).strftime("%m/%d/%Y, %H:%M:%S")
    end_datetime = datetime.datetime.fromtimestamp(since).strftime("%m/%d/%Y, %H:%M:%S")
    print("fetched data from {} to {}".format(start_datetime, end_datetime))

    with open(start_time_file, "w") as fout:
        json.dump({"start_time": since}, fout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_time', type=str, default="istheservicedown_march/start_time.json")
    parser.add_argument('-o', '--output_dir', type=str, default="istheservicedown_march")
    parser.add_argument('-c', '--config_file', type=str, default="istheservicedown.json")
    args = parser.parse_args()
    main(start_time_file=args.start_time, output_dir=args.output_dir, config_file=args.config_file)
