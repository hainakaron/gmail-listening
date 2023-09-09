const CLOUD_RUN_URL = '';
const TOPIC_NAME = ''; //Insert the topic name you created on Google Cloud Pub/Sub
const EMAIL_ADDRESS = ''; //Enter the email address of the account you want to listen to
const SHEET_ID = ''; //Enter the sheet id of your logger

function doPost(e) {
  let endpoint = '' //Enter the endpoint of your callback

  let message = JSON.parse(e.postData.getDataAsString()).message;
  let data = JSON.parse(Utilities.newBlob(Utilities.base64Decode(message.data)).getDataAsString());
  let historyId = data.historyId;
  
  //call back is a flask app on Google Cloud Run
  let result = UrlFetchApp.fetch(
    `${CLOUD_RUN_URL}/${endpoint}`,
    {method: 'GET', headers: {accept: 'application/json'}, muteHttpExceptions: true}).getContentText();
  
  //write logs to sheets
  let ss = SpreadsheetApp.openById(SHEET_ID).getSheetByName('doPost Logs')
  ss.appendRow([data, historyId, result]);
  
  return 200; //Always return success code
}

//dummy function, we don't really need this
function doGet(e) {
  Logger.log('doGet() was called');
  Logger.log(e);
  return HtmlService.createHtmlOutput("200");
}

//Reference: https://developers.google.com/gmail/api/reference/rest/v1/users/watch
function enrol_email() {
  var watchRes = Gmail.newWatchRequest();
  watchRes.labelIds = ['SENT'];
  watchRes.labelFilterAction = "include";
  watchRes.topicName = TOPIC_NAME; 
  var response = Gmail.Users.watch(watchRes, EMAIL_ADDRESS);
}