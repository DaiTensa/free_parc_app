from scrapy.crawler import CrawlerProcess
from pbfcrwal.spiders.pbf_nord_pas_de_calais_spider import PbfNordPasDeCalaisSpider

process = CrawlerProcess()
process.crawl(PbfNordPasDeCalaisSpider)
process.start()
