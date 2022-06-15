import scrapy
from scrapy.loader import ItemLoader
from A.items import AItem
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose
import sqlite3
from scrapy.exceptions import DropItem


##### spiders/wiki.py
###################################
class WikiSpider(scrapy.Spider):
	name = 'wiki'
	start_urls = [
		'https://www.scrapethissite.com/pages/simple/'
	]

	def parse(self, response, **kwargs):
		for country in response.css('div.country'):
			l = ItemLoader(item=AItem(), selector=country)
			l.add_css('name', 'h3.country-name')
			l.add_css('capital', 'span.country-capital::text')
			l.add_css('population', 'span.country-population::text')

			yield l.load_item()


##### items.py
###################################
def to_strip(value):
	return value.strip()

def to_upper(value):
	return value.upper()


class AItem(scrapy.Item):
	name = scrapy.Field(input_processor=MapCompose(remove_tags, to_strip, to_upper), output_processor=TakeFirst())
	capital = scrapy.Field(input_processor=MapCompose(remove_tags, to_strip), output_processor=TakeFirst())
	population = scrapy.Field(output_processor=TakeFirst())


##### pipelines.py
###################################
class APipeline:
    def __init__(self):
        self.con = sqlite3.connect('countries.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS countries(
            name TEXT PRIMARY KEY, capital TEXT, population INTEGER
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT OR IGNORE INTO countries VALUES (?, ?, ?)
        """, (item['name'], item['capital'], item['population']))
        self.con.commit()
        return item


class PopulationPipeline:
    def process_item(self, item, spider):
        if int(item['population']) < 50000000:
            raise DropItem('population is less than 50M...')
        return item


##### settings.py
###################################
ITEM_PIPELINES = {
   'A.pipelines.APipeline': 300,
   'A.pipelines.PopulationPipeline': 200,
}
