import matplotlib.pyplot as plt
import os
import argparse


def is_valid_post_file(filename, forum):
    return (forum in filename) and ('threads' not in filename)


def main(input_dir, forum, output_file):

    files = [x for x in os.listdir(input_dir) if is_valid_post_file(x, forum)]
    fig, ax = plt.subplots(figsize=(20, 8))
    time_ticks = list()
    for yr in (2019, 2020):
        for mth in range(1, 13):
            time_ticks.append("{}-{:02d}".format(yr, mth))

    time_ticks = time_ticks[0:len(time_ticks)-2]

    for file in files:
        month_count = dict()
        label = file.split(".tsv")[0][len(forum)+1:]

        with open(os.path.join(input_dir, file), "r") as fin:
            lines = fin.readlines()[1:]
        for line in lines:
            if len(line) > 1:
                tokens = line.replace("\n", "").split("\t")
                assert(len(tokens) == 6)
                month_count[tokens[1][:7]] = month_count.get(tokens[1][:7], 0) + 1

        y_vals = [month_count.get(x, 0) for x in time_ticks]
        ax.plot(list(range(len(time_ticks))), y_vals, label=label)

    ax.legend()
    ax.set_xlabel('time')
    ax.set_ylabel('number of posts')
    ax.set_title('Plot of post counts on {} in 2019 and 2020'.format(forum))
    ax.set_xticks(list(range(len(time_ticks))))
    ax.set_xticklabels(time_ticks)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    plt.savefig(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-f', '--forum', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()
    main(input_dir=args.input, forum=args.forum, output_file=args.output)
