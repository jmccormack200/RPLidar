'''
Last attempts with firebase python API didnt work,
Trying with just plain HTTP requests instead
'''
import requests, json

firebase_url = "https://radiant-torch-9117.firebaseio.com/users.json"

r = requests.get(firebase_url)
print r.status_code
print r.url
print r.text


'''
Per the firebase API docs:

Put updates the entry, but deletes what was there
Post updates the entry, leaving what was there, 
	and adds in a randomly generated string to ensure
	uniqueness

see: https://www.firebase.com/docs/rest/guide/saving-data.html
'''

json_string = json.dumps({'4':'Jackie Chan', '5': 'Chris Tucker', '6':'Johnny Bravo'})
#json_string = "Jackie Chan"
r = requests.put(firebase_url, data=json_string)
print r.url
print r.status_code
print r.text
