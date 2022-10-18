from __future__ import print_function
from datetime import datetime
import requests
import json
import cv2


BASE = "http://0.0.0.0:8000"
test_url = BASE + '/api/uploadimage'

img = cv2.imread('12345678.jpg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
a = img_encoded.tostring()

# prepare headers for http request
files = {'image': ('encoded.jpg', a, 'image/jpeg')}
data_dict = {'date': datetime.utcnow(), 'source': 'cam1' }
# send http request with image and receive response
response = requests.post(test_url, data = data_dict, files = files)
# decode response
#print(response.json())



































































