from secret import *
import urllib3
import json
import os

base_url = "https://graph.facebook.com/"


def send_request(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)

    return response


def show_err(response):
    err = json.loads(response.data.decode('utf-8'))

    print("Error!!! server sent:", response.status)
    print("message", err["error"]["message"])
    print("Terminating in 3 2 1...")
    exit(0)


def write_json_to_file(data, dir_name):
    with open(dir_name, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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


def get_group_post(group_id, group_name):
    limit = 1
    url = base_url + group_id + "/feed?limit=" + str(limit) + "&access_token=" + access_token

    if not os.path.isdir("./posts"):
        os.mkdir("./posts")

    # create a folder for the particular group
    if not os.path.isdir("./posts/" + group_name):
        os.mkdir("./posts/" + group_name)

    # get posts once at a time
    # get all the comments of that post
    # write it in a file and save it
    while True:
        response = send_request(url)
        if response.status != 200:
            show_err(response)
        else:
            post = {}
            data = json.loads(response.data.decode('utf-8'))

            # data["data"] is an array which has a length of limit which is 1 in this case
            if len(data["data"]) == 0:
                continue
            if "message" not in data["data"][0]:
                continue

            post["post"] = data["data"][0]["message"]
            post["comments"] = []
            post_id = data["data"][0]["id"]

            # get the comments. not using limit as param here
            # if params are given then paging will provide next url
            # not sure if it all the comments come if limit is not used
            comment_url = base_url + str(post_id) + "/comments?access_token=" + access_token
            while True:
                comment_response = send_request(comment_url)
                if comment_response.status != 200:
                    show_err(comment_response)
                else:
                    comment_data = json.loads(comment_response.data.decode('utf-8'))
                    for j in range(len(comment_data["data"])):
                        if "message" in comment_data["data"][j]:
                            post["comments"].append(comment_data["data"][j]["message"])

                    if "next" in comment_data["paging"]:
                        comment_url = comment_data["paging"]["next"]
                    else:
                        break

            if "next" in data["paging"]:
                url = data["paging"]["next"]
            else:
                break

            write_json_to_file(post, "./posts/" + group_name + "/" + post_id + ".json")
