import pickle
import argparse

# convert the output of disqus_list_thread.py to readable TSV file.

def main(input_file, output_file):
    with open(input_file, "rb") as fin:
        joint_response = pickle.load(fin)

    thread_list = list()
    seen_threads = set()
    for response in joint_response:
        thread_info = {
            "title": response['title'].replace("\n", " "),
            "threadId": int(response['id']),
            "url": response['signedLink'],
            "posts": int(response['posts'])
        }
        if thread_info["threadId"] not in seen_threads:
            thread_list.append(thread_info)
            seen_threads.add(thread_info["threadId"])

    thread_list = sorted(thread_list, key=lambda x: -1 * x['posts'])
    with open(output_file, "w") as fout:
        fout.write("title\tthreadId\turl\tposts\n")
        for t in thread_list:
            fout.write("{}\t{}\t{}\t{}\n".format(
                t["title"], t["threadId"], t["url"], t["posts"]
            ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True)
    parser.add_argument('-o', '--output_file', type=str, required=True)
    args = parser.parse_args()
    main(input_file=args.input_file, output_file=args.output_file)
