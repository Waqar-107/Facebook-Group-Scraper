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
   
   
#### Codes
1. secret.py - contains the access token and kept in the .gitignore file for obvious reasons.
2. groupHandler.py - has the main codes to get all the groups the user is in and group posts.
 * 
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