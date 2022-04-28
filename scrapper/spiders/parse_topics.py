from scrapy import Request

from scrapper.items import TopicItem


def parse_topics(response, base_url, parse_posts):
    topics_urls_path: str = "//td[@class='mfd-item-subject']/a"

    for topic_url in response.xpath(topics_urls_path):
        topic = TopicItem()

        topic_css = topic_url.css
        topic_href = topic_css('a::attr(href)')

        topic_item_url = base_url + topic_href.get().rpartition('&')[0]

        topic['topic_id'] = int(topic_href.re('\d+')[0])
        topic['topic_name'] = topic_css('a::text').get()
        topic['topic_url'] = topic_item_url
        topic['topic_main_num_page'] = response.meta['topic_page']

        yield topic
        yield Request(
            url=topic_item_url,
            callback=parse_posts,
            meta={
                'topic': topic,
            },
        )
