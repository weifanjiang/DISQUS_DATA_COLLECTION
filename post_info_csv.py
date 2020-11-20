import pickle
import argparse


def main(post_file, thread_file, output_file):

    with open(post_file, "rb") as fin:
        posts = pickle.load(fin)

    id2thread = None
    if thread_file is not None:
        with open(thread_file, "rb") as fin:
            threads = pickle.load(fin)
        id2thread = dict()
        for thread in threads:
            id2thread[int(thread["id"])] = thread["title"]

    post_list = list()
    for post in posts:
        try:
            post_formatted = {
                'id': post['id'],
                'createdAt': post['createdAt'],
                'username': post['author'].get('username', 'unavailable'),
                'forum': post['forum'],
                'thread': int(post['thread']),
                'raw_message': post['raw_message'].replace('\n', ' ')
            }
            if id2thread is not None:
                post_formatted['thread'] = id2thread.get(post_formatted['thread'], 'thread not found')
            post_list.append(post_formatted)
        except:
            print(post)

    post_list = sorted(post_list, key=lambda x: x['createdAt'])
    with open(output_file, 'w') as fout:
        fout.write("id\tcreatedAt\tusername\tforum\tthread\traw message\n")
        for post in post_list:
            fout.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
                post['id'], post['createdAt'], post['username'], post['forum'], post['thread'], post['raw_message']
            ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--post_file', type=str, required=True)
    parser.add_argument('-t', '--thread_file', type=str, required=False)
    parser.add_argument('-o', '--output_file', type=str, required=True)
    args = parser.parse_args()
    main(post_file=args.post_file, thread_file=args.thread_file, output_file=args.output_file)
