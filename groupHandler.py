from secret import *
import urllib3
import json

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


def get_group_post(group_id, limit):
    url = base_url + group_id + "/feed?limit=" + str(limit) + "&access_token=" + access_token
    response = send_request(url)

    if response.status != 200:
        show_err(response)
    else:
        print(response)
