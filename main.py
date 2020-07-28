# from dust i have come, dust i will be

from groupHandler import *
from secret import group_name

group_id = "null"
my_groups = get_my_groups()
for i in range(len(my_groups)):
    if my_groups[i]["name"] == group_name:
        group_id = my_groups[i]["id"]

get_group_post(group_id, group_name)
