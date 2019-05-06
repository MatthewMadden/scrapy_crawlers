import scrapy
from scrapy.crawler import CrawlerProcess

class DC_Chapter_Spider( scrapy.Spider ):

	name = "dc_chapter_spider"

	def start_requests( self ):
		url = 'https://www.datacamp.com/courses/all'
		yield scrapy.Request( url = url, callback = self.parse_front )

	def parse_front( self, response ):
		"""Code to parse the front courses page"""
		# Narrow in on the course blocks
		course_blocks = response.css( 'div.course-block' )
		# Direct to the course links
		course_links = course_blocks.xpath( './a/@href' )
		# Extract the links (as a list of strings)
		links_to_follow = course_links.extract()
		# Follow the links to the next parser
		for url in links_to_follow:
			yield response.follow( url = url, callback = self.parse_pages )

	def parse_pages( self, response ):
		"""Code to parse course pages"""
		# Direct to the course title text
		crs_title = response.xpath(  '//h1[contains(@class,"header-hero__title")]/text()' )
		# Extract and clean the course title text
		crs_title_ext = crs_title.extract_first().strip()
		# Direct to the chapter titles text
		ch_titles = response.css( 'h4.chapter__title::text' )
		# Extract and clean the chapter titles text
		ch_titles_ext = [t.stip() for t in ch_titles.extract()]
		# Store this in our dictionary
		dc_dict[ crs_title_ext ] = ch_titles_ext

dc_dict = dict()

process = CrawlerProcess()
process.crawl(DC_Chapter_Spider)
process.start() 
