import requests
from bs4 import BeautifulSoup
import re


qualities = {
	'144': 0,
	'240': 1,
	'360': 2,
	'480': 3,
	'720': 4,
	'1080': 5
}


class QualityError(Exception):
	pass


class Scraper:
	def __init__(self, url, quality):
		self.url = url
		self.quality = quality

	def get_all_links(self):
		"""
		takes `url` and brings all links available
		"""
		result = requests.get(self.url)
		content = BeautifulSoup(result.text, 'html.parser')
		video_links = content.find_all('a', href=re.compile('.mp4'))
		links = [link['href'] for link in video_links]
		return links

	def get_link(self):
		"""
		return the user requested quality, if not available raise QualityError
		"""
		links = self.get_all_links()
		available_qualities = self.get_qualities()
		if self.quality not in available_qualities:
			raise QualityError(f'This quality is not avalable \n available qualities are {available_qualities}')
		else:
			link = links[qualities[self.quality]]
			return link

	def get_qualities(self):
		"""
		return all available qualities
		"""
		links = self.get_all_links()
		qua = list(qualities.keys())
		available_qualities = []
		for i in range(len(links)):
			available_qualities.append(qua[i])
		return available_qualities


class Main:
	def __init__(self, url, quality):
		self.url = url
		self.quality = quality
		self.scraper = Scraper(url, quality)

	def download(self):
		video_url = str(self.scraper.get_link())
		with open('video.mp4', 'wb') as f:
			print('Downloading...')
			result = requests.get(video_url, stream=True)
			total = result.headers.get('content-length')

			if total is None:
				f.write(result.content)
			else:
				download = 0
				total = int(total)
				for data in result.iter_content(chunk_size=4096):
					download += len(data)
					f.write(data)
					done = int(50*download / total)
					print("\r[%s%s]" % ('=' * done, ' ' * (50-done)), end='')
		print('\nVideo downloaded...')


a = Main(url='https://www.namasha.com/v/cfUTOERr', quality='240')
a.download()
