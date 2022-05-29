import requests
from bs4 import BeautifulSoup


url = 'https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_episodes'

response = requests.get(url)
content = BeautifulSoup(response.text, 'html.parser')

episodes = []
ep_tables = content.select('table.wikiepisodetable')

for table in ep_tables:
	headers = []
	rows = table.find_all('tr')

	for header in table.find('tr').find_all('th'):
		headers.append(header.text)

	for row in table.find_all('tr')[1:]:
		values = []
		for col in row.find_all(['th', 'td']):
			values.append(col.text)

		if values:
			episode_dict = {headers[i]:values[i] for i in range(len(values))}
			episodes.append(episode_dict)

for ep in episodes:
	print(ep)
