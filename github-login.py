import requests
from bs4 import BeautifulSoup


session = requests.Session()

url = 'https://github.com/{}'
username = 'amirbigg'

r = session.get(url.format('login'))
content = BeautifulSoup(r.text, 'html.parser')

data = {}
for form in content.find_all('form'):
	for inp in form.select('input[type=hidden]'):
		data[inp.get('name')] = inp.get('value')

data.update({'login':'', 'password':''})

r = session.post(url.format('session'), data=data)
r = session.get(url.format(username))
content = BeautifulSoup(r.text, 'html.parser')
user_info = content.find(class_='vcard-details')
print(user_info.text)
