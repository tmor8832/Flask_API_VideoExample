from datetime import date
from flask import Flask, render_template, request, url_for, flash, redirect, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
import tempfile
import jsonpickle
import numpy as np
import cv2
import os
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
import mysql.connector
from mysql.connector import errorcode

config = {
  'host':'jhub123aa.mysql.database.azure.com',
  'user':'azureuser',
  'password':'123456Aa',
  'database':'event1',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/etc/ssl/certs/DigiCertGlobalRootG2.crt.pem',
}
 
# IMPORTANT: Replace connection string with your storage account connection string
# Usually starts with DefaultEndpointsProtocol=https;...
MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=eventmedia123aa;AccountKey=UJOGjkFZIINqpF8t7/3VdI+0sDQEEBaOSNH+7KlsHT90utYD7JoKv2ARfXugdVbZSfFy1oAEK/Ax+AStFv/fMg==;EndpointSuffix=core.windows.net"
 
# Replace with blob container. This should be already created in azure storage.
MY_IMAGE_CONTAINER = "images"
 
# Replace with the local folder which contains the image files for upload
 
class AzureBlobFileUploader:
  def __init__(self):
    # Initialize the connection to Azure storage account
    self.blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    
  def upload_image(self,file_name):
    name = str(uuid.uuid4())
    # Create blob with same name as local file name
    blob_client = self.blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER,
                                                          blob=name)
    # Create blob on storage
    # Overwrite if it already exists!
    image_content_setting = ContentSettings(content_type='image/jpeg')
    print(f"uploading file - {name}")

    with open(file_name, "rb") as data:
      blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)
      print('Link to image is: https://eventmedia123aa.blob.core.windows.net/images/' +name)
    
    return ('https://eventmedia123aa.blob.core.windows.net/images/' +name)
    

app = Flask(__name__)
api = Api(app)

CORS(app) #enable routes from other parts of the network without blocking the requests

@app.route('/api/uploadimage', methods=['POST'])
def upload():
    print('I am entering here')
    conn = mysql.connector.connect(**config)
    print("Connection established")
    cursor = conn.cursor()
    ''' The first time the function is executed to create the table uncomment this and use it, once created no longer needed'''
    # Drop previous table of same name if one exists
    #cursor.execute("DROP TABLE IF EXISTS eventinit;")
    #print("Finished dropping table (if existed).")
#    # Create table
    cursor.execute("CREATE TABLE test12(id serial PRIMARY KEY AUTO_INCREMENT, date VARCHAR(50) NOT NULL, source VARCHAR(50) NOT NULL, link VARCHAR(500) NOT NULL);")
    #print("Finished creating table.")
    # Insert some data into table
    img = (request.files['image'].read())
    date_info = str(request.form['date'])
    source = request.form['source']
    source = str(source)
# convert string of image data to uint8
    nparr = np.frombuffer(img, np.uint8)
    filename = '/tmp/image.jpg' 
    temp = open(filename, 'w+b')
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print(date_info)
    cv2.imwrite(str(temp.name), img)
    print(temp.name)
    azure_blob_file_uploader = AzureBlobFileUploader()
    link = azure_blob_file_uploader.upload_image(temp.name)
    print(link)
    print(len(link))
    cursor.execute("INSERT INTO test12 (date, source, link) VALUES (%s, %s, %s);", (date_info, source, link))
    print("Inserted",cursor.rowcount,"row(s) of data.")
    conn.commit()
    cursor.close()
    conn.close()
# build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]), 'Link' : link, 'Date': date_info, 'Source': source
            }
# encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
