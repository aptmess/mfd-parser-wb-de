import typing as t

from scrapy import Request
from scrapy.http import Response


def parse_posts(
    response: Response,
    base_url: str,
    parse_comments: t.Callable[[t.Any], t.Iterator[t.Any]],
) -> t.Iterator[t.Any]:
    comments_page_pagination = response.xpath(
        "//a[@class='mfd-paginator-selected']/text()"
    )

    topic_id = response.meta['topic']['topic_id']

    current_posts_pages_count = int(comments_page_pagination.get())

    if current_posts_pages_count == 1:
        yield Request(
            url=f'{base_url}/forum/thread/?id={topic_id}&page=1',
            callback=parse_comments,
            meta={'topic': response.meta['topic'], 'post_page': 1},
        )
        yield Request(
            url=f'{base_url}/forum/thread/?'
            f"id={response.meta['topic']['topic_id']}&page=10000000",
            callback=parse_comments,
            meta={
                'topic': response.meta['topic'],
                'post_page': 1,
            },
        )

    else:
        current_page_num = 1

        while current_page_num <= current_posts_pages_count:
            topic_page = current_page_num - 1
            yield Request(
                url=f'{base_url}/forum/thread/?'
                f"id={response.meta['topic']['topic_id']}"
                f'&page={topic_page}',
                callback=parse_comments,
                meta={
                    'topic': response.meta['topic'],
                    'post_page': topic_page,
                },
            )
            current_page_num += 1

        yield Request(
            url=f'{base_url}/forum/thread/?'
            f"id={response.meta['topic']['topic_id']}&page=10000000",
            callback=parse_comments,
            meta={
                'topic': response.meta['topic'],
                'post_page': current_page_num - 2,
            },
        )
