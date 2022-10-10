import requests

BASE = "http://0.0.0.0:5000/" #default URL given when you run the flask file main.py

data = [{"date":"010719971200", "event": "Motion", "event_info":"Person", "event_link":""}, 
        {"date":"020719971300", "event": "Motion", "event_info":"Person", "event_link":"https://link.com"}]

for i in range(len(data)):
    response = requests.put(BASE + "event/", data[i])
    print(response)


input()
x = "5f9ef148-aa43-4629-82ae-dc2162cf703a"
response = requests.get(BASE + "event/" + str(x))
print(response.json())
input()
response = requests.delete(BASE + "event/" + str(x))
print(response.json())
input()
response = requests.get(BASE + "events/")
print(response.json())
input()
response = requests.put(BASE + "delevents/")