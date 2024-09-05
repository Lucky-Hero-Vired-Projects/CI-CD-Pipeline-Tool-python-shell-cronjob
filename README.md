# CI-CD-Pipeline-Tool-python-shell-cronjob

## Description

Create a complete CI-CD pipeline using bash, python, and crontabs. The list of tasks is specified below: 

__Task 1__ : Set Up a Simple HTML Project , 
Create a simple HTML project and push it to a GitHub repository. 

__Task 2__: Set Up an AWS EC2/Local Linux Instance with Nginx

__Task 3__: Write a Python Script to Check for New Commits, 
 Create a Python script to check for new commits using the GitHub API.

__Task 4__: Write a Bash Script to Deploy the Code, 
Create a bash script to clone the latest code and restart Nginx.

__Task 5__: Set Up a Cron Job to Run the Python Script, 
Create a cron job to run the Python script at regular intervals.

__Task 6__: Test the Setup 

Make a new commit to the GitHub repository and check that the changes are automatically deployed. 


### Steps: 

1. First created a Server
2. Install Nginx
3. Copy sample Index.html file to /var/www/html/ from Github local repo
4. check local and github repo all commits are equal or not using python
5. if not equal, the shell script will clone the latest code and copy index file to specified directory
6. restart the nginx servcies

cronjob setting: 

*/55 * * * *  /opt/github-commit-check.py

every 15 mins, pyhon script will execute
Pyhton will check commits from both loacl and github, if both are same will exit
both are different, python will start another shell script, this will clone the code, copy the latest data to nginx www folder and restart the nginx servcie.

