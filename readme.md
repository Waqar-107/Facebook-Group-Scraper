# Facebook-Group-Scraper

scraping public posts of a facebook group using facebook-graph-api

#### Before start coding:
1. create an app in https://developers.facebook.com/
2. generate an access token using this app.
3. add 2 permissions. 
   * groups_show_list
   * groups_access_member_info
4. become the admin of the group. without being admin the posts are not 
accessible and the server will reply with a 403 :) 
5. as we have to use sleep during the execution, we should extend the access_token, else ot will
expire within few hours. you can do this by opening the access token in debug mode. 
   
   
#### Codes
1. secret.py - contains the access token and kept in the .gitignore file for 
obvious reasons. also contains a variable called required_group_name that is the groups data we want to fetch
2. groupHandler.py - has the main codes to get all the groups the user is in and group posts.
    * send_request(url) - takes the url as a string, returns the response.
    * show_err(response) - takes the response object. if limit over then return true 
    else exits.
    * good_night(sec) - executes sleep() for sec seconds.
    * write_json_to_file(data, dir_name) - takes a dictionary data and writes in json 
    format in the specified file.
    * read_json_file(dir_name) - reads the specified file returns a dictionary.
    * get_my_groups() - returns array of dictionaries, containing group name and id, the 
    groups where the use is a member.
    * get_group_post(group_id, group_name, limit, sleep_time) - takes group-id and name and sleep_time and for each post 
    creates a json file and write the post there. stores the file in a folder that's 
    name is the group-name and file name is the post-id. sleeps for sleep_time if limit is over.
    * get_comments_of_group_post(post_id, group_name, sleep_time) - takes post id, sleep_time and the group name, 
    fetches comments of that post and writes on that same file where the main post was written.
    sleeps for sleep_time if limit is over.
    can be called inside a loop.
3. main.py - the driver


#### To-Do
1. fetch replies.
2. try to get user credential of those who posted/commented.
3. in order to get all the posts in a single execution might need a timer that
will pause the code execution and start after the limit to call api increases.
normally it goes from 0 to 100% and after a while it starts to decrease from 100 to 0.


#### Problems
1. it may be possible your limit to call api will be over if you 
want to get all the posts and comments of a group in a single execution.