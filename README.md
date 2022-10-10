# Flask Project with Azure Storage

Using Flask I created a simple flask app allowing information about events to be placed into a database. The db uses SQLAlchemy. The idea is for this to be linked to ML backend which will push event information to the database. The vue frontend will then use the db and flask with requests to give event information to the user. 

The azureupload code uploads images / videos to an azure storage account and this link can then be stored in the database and accessed by the vue app.

Each event is given a random ID using uuid

By hosting on 0.0.0.0 port 5000 I was able to acess the app from elsewhere on my network and make requests.

![image](https://user-images.githubusercontent.com/64171887/194876083-27d1cac4-4b69-478a-8cb6-aceb83c0bb13.png)

![image](https://user-images.githubusercontent.com/64171887/194876172-7fbfbabd-d38f-4adb-8c92-469db2ef8edf.png)

![image](https://user-images.githubusercontent.com/64171887/194876307-905e1a5c-8c3c-45f5-a8d0-6a47072e944c.png)


