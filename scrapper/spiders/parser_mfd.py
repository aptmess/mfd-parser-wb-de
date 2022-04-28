from scrapy import Request, Spider

from scrapper.spiders.parse_comments import parse_comments
from scrapper.spiders.parse_posts import parse_posts
from scrapper.spiders.parse_topics import parse_topics


class MFDSpider(Spider):
    name: str = 'mfd_spider'
    base_url: str = 'http://forum.mfd.ru'
    start_urls = ['http://forum.mfd.ru/forum/subforum/?id=649']
    handle_httpstatus_list = [301, 302]

    def parse_comments(self, response):
        yield from parse_comments(response, self.base_url)

    def parse_posts(self, response):
        yield from parse_posts(response, self.base_url, self.parse_comments)

    def parse_topics(self, response):
        yield from parse_topics(response, self.base_url, self.parse_posts)

    def parse(self, response, **kwargs):
        main_page_pagination = response.xpath(
            "//div[@class='mfd-paginator']/a/text()"
        )

        next_page_url: int = int(main_page_pagination.extract()[-1])

        current_page_num = 1

        while current_page_num <= next_page_url:

            topic_page = current_page_num - 1

            yield Request(
                f'{self.start_urls[0]}&page={topic_page}',
                callback=self.parse_topics,
                meta={'topic_page': topic_page},
            )

            current_page_num += 1
