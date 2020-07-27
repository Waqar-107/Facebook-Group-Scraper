# Facebook-Group-Scraper

scraping public posts of a facebook group using facebook-graph-api

#### Before start coding:
1. create an app in (https://developers.facebook.com/)[https://developers.facebook.com/]
2. generate an access token using this app.
3. add 2 permissions. 
   * groups_show_list
   * groups_access_member_info
   
#### codes
1. secret.py - contains the access token and kept in the gitignore file for obvious reasons.
2. groupHandler.py - has the main codes to get all the groups the user is in and group posts.
3. main.py - the driver