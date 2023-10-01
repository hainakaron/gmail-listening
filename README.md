This project peeks on sent emails in a Gmail account and logs it on Google Sheet.
It uses Google Cloud Run to host a Flask app that contains the callback of one of the functions in the Google Apps Script project
The callback checks the sent emails and its body, then saves it on the log that is a Google Sheet

HOW TO SETUP
# Google Cloud Console
1. Create a project and enable billing. Refer to https://developers.google.com/workspace/guides/get-started
2. Grab the Project ID, you will need this on # Google Apps Script# Google Apps Script section
3. Configure OAuth consent. Refer to https://developers.google.com/workspace/guides/configure-oauth-consent#configure_oauth_consent

# Writing on Google Sheets for your logs
1. Create a service account to allow our project to write on google sheets. Refer to https://cloud.google.com/iam/docs/service-accounts-create
2. Create a key for the service account by clicking on the service account -> Keys -> Add Key. A JSON file will be downloaded
3. Store the JSON file on this project inside the gcp folder
4. Rename the file with 'service_account.json'
5. Get the service account's email
6. Create a Google sheet and share Editor access to the service account's email

# Create OAuth 2.0 Client IDs for the Flask App
This service account will  be responsible for accessing the GMail account
1. On APIs and Services, create a 0Auth Client ID. Refer to https://support.google.com/cloud/answer/6158849?hl=en
2. Name can be 'credentials_local' and application Type is Desktop App
3. Click Download JSON and store it on this project inside the gcp folder
5. Rename the file with credentials_local.json

# Deploy Flask app to Cloud Run
1. Create your own repo of this project on Github
2. Go to Cloud Run
3. Create a service
4. Select Continuously deploy new revisions from a source repository. This will automatically update the app on cloud run whenever changes are made to the repository (depending on the branch you select for the service)
5. Click Set up with Cloud Build
6. For the repository provider, you can use Cloud Source Repository for more security. For the mean time use Github. Make sure to share the access to Cloud Run on your repository. Then click Next
7. Select the branch you want
8. For build type, use Dockerfile, then hit Save
9. For Authentication, select Allow unauthenticated invocations then click Create
10. Wait for the build to finish
11. When done, grab the URL, you will need it on # Google Apps Script section

# Create a Topic
1. Go to Pub/Sub and create a Topic. Refer to https://cloud.google.com/pubsub/docs/create-topic
2. Grab the Topic Name, you will need this on # Google Apps Script section

# Google Apps Script
1. Create a script on https://www.google.com/script/start/
2. Copy the contents of gmail_notify.js and paste it to the script
3. On the sidebar, click the + button beside Service
4. Select GMail API. This will allow you to use the GMail library on the script
5. Next, go to the gear icon to open Settings
6. Scroll down to Google Cloud Platform (GCP) Project section
7. Click Change Project and enter the Project ID from # Google Cloud Console section as the GCP Project Number
8. Click Set project
9. Review the code and provide value for the constants
10. Enrol the email address of the account you want to spy on by running the enrol_email() function
11. A pop up window for Authorization will show, click Review Permission, and log in to the Gmail account, then click Allow
12. You should then see something like this '{ expiration: '1694875429850', historyId: '60864326' }' on the Execution log indicating that the enrolment is successful
13. Click Deploy -> New Deployment
14. Click Gear Icon for the type, then select Web app
15. Give it a description such as V1 then, then choose Anyone for Who has access, then click Deploy
16. Copy the Web app URL, open a new tab on the browser and load the URL - a new url will be generated
17. Copy the generated URL and go to Pub/Sub
18. Under the topic created in the previous section, create a Subscription. 
19. Under the Delivery Type, select Push
20. On the endpoint URL, paste the URL from step 17 then hit Create

# Create OAuth 2.0 Client IDs for the Google Apps Script Web App
1. Create another 0Auth Client ID
2. Name can be 'credentials_web' and Application Type is Web application
3. Under Authorized redirect URIs, add a URI and paste the generated URL from step 17 of the previous section, then click Create

# Create a token to allow your Flask app peek on the emails on the Gmail Account
1. Run the main.py by entering 'python main.py' on your terminal.
2. After running, a token.pickle file should be added to the project
3. Commit this file to your repo. Your Flask app on Cloud Run will use this token to access the Gmail account you are spying on
