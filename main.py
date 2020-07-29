# from dust i have come, dust i will be

from groupHandler import *
from secret import required_group_name

group_id = "null"

# reset the log file
reset_log_file()

my_groups = get_my_groups()
for i in range(len(my_groups)):
    if my_groups[i]["name"] == required_group_name:
        group_id = my_groups[i]["id"]

print(group_id)
get_group_post(group_id, required_group_name, 600, 100)