import scrapy

from scrapy.loader import ItemLoader

from ..items import QnbItem
from itemloaders.processors import TakeFirst


class QnbSpider(scrapy.Spider):
	name = 'qnb'
	start_urls = ['https://www.qnb.com/sites/qnb/qnbglobal/page/en/ennews.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="page-subpage-content"]/p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="page-subpage-content"]/text()[normalize-space()]').get()

		item = ItemLoader(item=QnbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
