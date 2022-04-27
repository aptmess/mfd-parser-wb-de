from scrapy import Request, Spider

from app.services.pipeline import Compose
from app.services.transformers import (
    AuthorID,
    AuthorName,
    PostAnsweredPosts,
    PostCreatedAt,
    PostIDTransformer,
    PostIsDeletedTransformer,
    PostRating,
    PostText,
)
from scrapy_mfd.items import AuthorItem, PostItem, TopicItem
from scrapy_mfd.paths import AnonymousAuthorLinks, AUTHORLinks, POSTLinks


class MFDSpider(Spider):
    name: str = 'mfd_spider'
    base_url: str = 'http://forum.mfd.ru'
    start_urls = ['http://forum.mfd.ru/forum/subforum/?id=649']

    def parse_comments(self, response):
        for post in response.xpath(
            "//div[@class='mfd-post' or @class='mfd-post mfd-post-deleted']"
        ):
            post_item = PostItem()
            author_item = AuthorItem()

            author_compose = Compose(
                [
                    [
                        AuthorID(AUTHORLinks.author_id, 'author_id', post),
                        AuthorID(
                            AnonymousAuthorLinks.author_id, 'author_id', post
                        ),
                    ],
                    [
                        AuthorName(
                            AUTHORLinks.author_name, 'author_name', post
                        ),
                        AuthorName(
                            AnonymousAuthorLinks.author_name,
                            'author_name',
                            post,
                        ),
                    ],
                ]
            )

            author, result = author_compose(author_item)

            if not result:
                continue

            post_compose = Compose(
                [
                    PostIDTransformer(POSTLinks.post_id, 'post_id', post),
                    PostText(POSTLinks.post_text, 'post_text', post),
                    PostCreatedAt(
                        POSTLinks.created_at, 'post_created_at', post
                    ),
                    PostRating(POSTLinks.post_rating, 'post_rating', post),
                    PostIsDeletedTransformer(
                        POSTLinks.is_post_deleted, 'is_deleted', post
                    ),
                    PostAnsweredPosts(
                        POSTLinks.answered_posts_ids_path,
                        'related_to',
                        post,
                        get_all=True,
                    ),
                ]
            )
            post, result = post_compose(post_item)

            if result:
                post['post_url'] = (
                    f"{self.base_url}/forum/post/?id={post['post_id']}"
                    f"&page={response.meta['post_page']}"
                )
                post['topic_id'] = response.meta['topic']['topic_id']
                post['author_id'] = author['author_id']
                for item in [author, post]:
                    yield item

    def parse_posts(self, response):
        comments_page_pagination = response.xpath(
            "//a[@class='mfd-paginator-selected']/text()"
        )

        topic_id = response.meta['topic']['topic_id']

        current_posts_pages_count = int(comments_page_pagination.get())
        if current_posts_pages_count == 1:
            yield Request(
                url=f'{self.base_url}/forum/thread/?id={topic_id}&page=1',
                callback=self.parse_comments,
                meta={'topic': response.meta['topic'], 'post_page': 1},
            )

        else:
            current_page_num = 1

            while current_page_num <= current_posts_pages_count:
                topic_page = current_page_num - 1
                yield Request(
                    url=f'{self.base_url}/forum/thread/?'
                    f"id={response.meta['topic']['topic_id']}"
                    f'&page={topic_page}',
                    callback=self.parse_comments,
                    meta={
                        'topic': response.meta['topic'],
                        'post_page': topic_page,
                    },
                )
                current_page_num += 1

    def parse_topics(self, response):
        topics_urls_path: str = "//td[@class='mfd-item-subject']/a"

        for topic_url in response.xpath(topics_urls_path):
            topic = TopicItem()

            topic_css = topic_url.css
            topic_href = topic_css('a::attr(href)')

            topic_item_url = self.base_url + topic_href.get().rpartition('&')[0]

            topic['topic_id'] = int(topic_href.re('\d+')[0])
            topic['topic_name'] = topic_css('a::text').get()
            topic['topic_url'] = topic_item_url
            topic['topic_main_num_page'] = response.meta['topic_page']
            yield topic
            yield Request(
                url=topic_item_url,
                callback=self.parse_posts,
                meta={
                    'topic': topic,
                },
            )

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
