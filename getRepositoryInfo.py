import requests
username = 'username'
password = 'pass'
#https://api.github.com/repos/rust-lang-nursery/edition-guide/issues
rep_url = "https://api.github.com/repos/Automattic/wp-calypso/issues?state=all&page=1";
headers = {'Accept': 'application/vnd.github.squirrel-girl-preview'}
r = requests.get(url=rep_url,  auth=(username, password) , headers=headers)
rep_data_req = r.json()
page = 1
rep_data = []
while rep_data_req != []:
	print (page)
	page = page + 1
	rep_data = rep_data + rep_data_req
	rep_url = "https://api.github.com/repos/Automattic/wp-calypso/issues?state=all&page=" + str(page);
	r = requests.get(url=rep_url, auth=(username, password), headers=headers)
	rep_data_req = r.json()
	
import json
with open('Automattic_wp-calypso.json', 'w') as outfile:
    json.dump(rep_data, outfile)
