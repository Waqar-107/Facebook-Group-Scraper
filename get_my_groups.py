from secret import *
import urllib3
import json


def send_request(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)

    return response


def get_my_groups():
    url = "https://graph.facebook.com/me/groups?access_token=" + access_token

    my_groups = []
    while True:
        response = send_request(url)
        if response.status != 200:
            print("Error!!! server sent:", response.status)
            print("Terminating in 3 2 1...")
            exit(0)
        else:
            data = json.loads(response.data.decode('utf-8'))
            for i in range(len(data["data"])):
                my_groups.append(data["data"][i])

            if "next" in data["paging"]:
                url = data["paging"]["next"]
            else:
                break
    return my_groups
