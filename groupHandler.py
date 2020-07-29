from secret import *
from util import *
import urllib3
import json
import os
import time

logFile = open("log.txt", "w");
count = 0


def send_request(url):
    global count

    http = urllib3.PoolManager()
    response = http.request("GET", url)
    count += 1

    return response


def show_err(response):
    err = json.loads(response.data.decode('utf-8'))

    logFile.write("Error!!! server sent: " + str(response.status) + "\n")
    logFile.write("message: " + err["error"]["message"] + "\n")

    if err["error"]["code"] in error_codes:
        return True

    logFile.write("Terminating in 3 2 1...\n")
    exit(0)


def good_night(sec):
    global count

    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)

    logFile.write("limit over after " + str(count) + "requests\n")
    logFile.write("Current time is " + result + "\n")

    time.sleep(sec)

    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    logFile.write("Waking up at " + result + "\n")

    count = 0


def write_json_to_file(data, dir_name):
    with open(dir_name, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_json_file(dir_name):
    with open(dir_name, 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_my_groups():
    url = base_url + "me/groups?access_token=" + access_token

    my_groups = []
    while True:
        response = send_request(url)
        if response.status != 200:
            show_err(response)
        else:
            data = json.loads(response.data.decode('utf-8'))
            for i in range(len(data["data"])):
                my_groups.append(data["data"][i])

            if "next" in data["paging"]:
                url = data["paging"]["next"]
            else:
                break

    return my_groups


def get_group_post(group_id, group_name, sleep_time, limit):
    url = base_url + group_id + "/feed?limit=" + str(limit) + "&access_token=" + access_token

    if not os.path.isdir("./posts"):
        os.mkdir("./posts")

    # create a folder for the particular group
    if not os.path.isdir("./posts/" + group_name):
        os.mkdir("./posts/" + group_name)

    # get posts, "limit"s at a time and keep calling if there's next
    # write it in a file and save it
    while True:
        response = send_request(url)
        if response.status != 200:
            if show_err(response):
                good_night(sleep_time)
                continue
        else:
            post = {}
            data = json.loads(response.data.decode('utf-8'))
            print(data)
            # data["data"] is an array which has a length of limit which is 1 in this case
            for i in range(len(data["data"])):
                if "message" not in data["data"][i]:
                    continue

                post["post"] = data["data"][i]["message"]
                post["id"] = data["data"][i]["id"]

                write_json_to_file(post, "./posts/" + group_name + "/" + post["id"] + ".json")

            if "paging" in data and "next" in data["paging"]:
                url = data["paging"]["next"]
            else:
                break


def get_comments_of_group_post(post_id, group_name, sleep_time):
    post = read_json_file("./posts/" + group_name + "/" + post_id + ".json");

    # get the comments. not using limit as param here
    # if params are given then paging will provide next url
    # not sure if it all the comments come if limit is not used
    comment_url = base_url + str(post_id) + "/comments?access_token=" + access_token
    post["comments"] = []

    while True:
        comment_response = send_request(comment_url)
        if comment_response.status != 200:
            if show_err(comment_response):
                good_night(sleep_time)
        else:
            comment_data = json.loads(comment_response.data.decode('utf-8'))
            for j in range(len(comment_data["data"])):
                if "message" in comment_data["data"][j]:
                    post["comments"].append(comment_data["data"][j]["message"])

            if "next" in comment_data["paging"]:
                comment_url = comment_data["paging"]["next"]
            else:
                break

    write_json_to_file(post, "./posts/" + group_name + "/" + post_id + ".json")
