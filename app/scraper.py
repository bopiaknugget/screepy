# scraper.py
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.item import Item, Field
from bs4 import BeautifulSoup
import crochet
from twisted.internet.error import TimeoutError, DNSLookupError
import logging

crochet.setup()
logger = logging.getLogger(__name__)

class ContentItem(Item):
    url = Field()
    content = Field()
    error = Field()

class RobustContentSpider(scrapy.Spider):
    name = 'robust_spider'

    def __init__(self, url=None):
        super().__init__()
        self.start_urls = [url] if url else []
        self.custom_settings = {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'DOWNLOAD_TIMEOUT': 15,
            'RETRY_TIMES': 2
        }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errback)

    def parse(self, response):
        logger.info(f"Scraping URL: {response.url}")
        try:
            if response.status != 200:
                yield ContentItem(url=response.url, error=f"HTTP {response.status}")
                return

            text = self.clean_html(response.text)
            if not text:
                yield ContentItem(url=response.url, error="No main content detected")
            else:
                yield ContentItem(url=response.url, content=text)

        except Exception as e:
            logger.exception("Exception during parsing")
            yield ContentItem(url=response.url, error=f"Parsing error: {str(e)}")

    def clean_html(self, html_text):
        soup = BeautifulSoup(html_text, 'lxml')
        main = soup.find('main') or soup.find('article') or soup.body
        if not main:
            return None

        for tag in main(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        return main.get_text(separator='\n', strip=True)

    def errback(self, failure):
        request = failure.request
        error_msg = "Network timeout/DNS failure" if failure.check(TimeoutError, DNSLookupError) else str(failure.value)
        logger.warning(f"Error fetching {request.url}: {error_msg}")
        yield ContentItem(url=request.url, error=error_msg)

@crochet.wait_for(timeout=30.0)
def run_scraper(url):
    runner = CrawlerRunner()
    items = []

    def _collect(item):
        items.append(item)

    crawler = runner.create_crawler(RobustContentSpider)
    crawler.signals.connect(_collect, scrapy.signals.item_scraped)

    deferred = runner.crawl(crawler, url=url)
    deferred.addCallback(lambda _: items)
    return deferred
