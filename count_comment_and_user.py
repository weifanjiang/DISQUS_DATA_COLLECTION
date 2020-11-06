import os
import matplotlib.pyplot as plt

dir = "istheservicedown"
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(".tsv")]
records = list()
for file in files:
    print(file)
    with open(os.path.join(dir, file), "r") as fin:
        records += fin.readlines()[1:]
print("total num of comments: {}".format(len(records)))

users = dict()
posts = dict()

for record in records:
    tokens = record.split("\t")
    time = tokens[1]
    user = tokens[2]

    year, month = time.split("T")[0].split("-")[0:2]
    if int(year) == 2020:
        month = int(month)
        user_set = users.get(month, set())
        user_set.add(user)
        users[month] = user_set
        posts[month] = posts.get(month, 0) + 1

months = list(range(1, 12))
plt.plot(months, [len(users[x]) for x in months], label="active users per month")
plt.plot(months, [posts[x] for x in months], label="num of posts per month")
plt.legend()
plt.title("Activities on isTheServiceDown.com in 2020")
plt.show()
