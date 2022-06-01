import requests
from bs4 import BeautifulSoup
import re


url = 'https://github.com/{}'
username = 'amirbigg'

r = requests.get(url.format(username), params={'tab': 'repositories'})
html_soup = BeautifulSoup(r.text, 'html.parser')
repos_element = html_soup.find(id='user-repositories-list')
repos = repos_element.find_all('li')

for repo in repos:
	name = repo.find('h3').find('a').get_text(strip=True)
	language = repo.find(attrs={'itemprop': 'programmingLanguage'})
	language = language.get_text(strip=True) if language else 'unknown'
	stars = repo.find('a', attrs={'href': re.compile('\/stargazers')})
	stars = int(stars.get_text(strip=True).replace(',', '')) if stars else 0
	print(name, language, stars)
