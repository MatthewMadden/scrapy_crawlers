import scrapy
from scrapy.crawler import CrawlerProcess

#Create the spider class
class DCspider( scrapy.Spider ):
	name = "dc_spider"
	# start_requests method
	def start_requests( self ):
		urls = ['https://www.datacamp.com/courses/all']
		for url in urls:
			yield scrapy.Request( url = url, callback = self.parse )
	
	"""Simple example: parse method for writing html structure
	of an entire webpage to a file"""
	# def parse( self, response ):
	# 	html_file = 'DC_courses.html'
	# 	with open( html_file, 'wb' ) as fout:
	# 		fout.write( response.body )

	"""More complex example: parse method for writing links
	for each course to a CSV file"""
	# def parse( self, response ):
	# 	links = response.css('div.course-block > a::attr(href)').extract()
	# 	filepath = 'DC_links.csv'
	# 	with open( filepath, 'w' ) as f:
	# 		f.writelines( [link + '\n' for link in links] )

	"""Even more complex: parse method for getting all links and
	then automatically crawling the page of each link collected"""
	def parse( self, response ):
		links = response.css('div.course-block > a::attr(href)').extract()
		for link in links:
			yield response.follow( url = link, callback = self.course_descr) 
	def course_descr( self, response ):
		# Extract course description
		course_descr = response.css('p.course__description::text').extract_first()
		# For now, just yield the course description
		yield course_descr


process = CrawlerProcess()

process.crawl(DCspider)

process.start()
