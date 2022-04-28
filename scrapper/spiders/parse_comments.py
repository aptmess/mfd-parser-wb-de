import typing as t

from scrapy.http import Response
from scrapy.utils.python import to_unicode
from six.moves.urllib.parse import urljoin

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
from scrapper.items import AuthorItem, PostItem
from scrapper.paths import AnonymousAuthorLinks, AUTHORLinks, POSTLinks


def parse_comments(response: Response, base_url: str) -> t.Iterator[t.Any]:
    for post in response.xpath(
        "//div[@class='mfd-post' or @class='mfd-post mfd-post-deleted']"
    ):
        post_item = PostItem()
        author_item = AuthorItem()

        author_compose = Compose(
            [
                [
                    AuthorID(AUTHORLinks.author_id, 'author_id', post),
                    AuthorID(AnonymousAuthorLinks.author_id, 'author_id', post),
                ],
                [
                    AuthorName(AUTHORLinks.author_name, 'author_name', post),
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
                PostCreatedAt(POSTLinks.created_at, 'post_created_at', post),
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
                f"{base_url}/forum/post/?id={post['post_id']}"
                f"&page={response.meta['post_page']}"
            )
            post['topic_id'] = response.meta['topic']['topic_id']
            post['author_id'] = author['author_id']
            for item in [author, post]:
                yield item

    if 300 <= response.status < 400:
        location = to_unicode(response.headers['location'].decode('latin1'))
        request = response.request
        redirected_url = urljoin(request.url, location)

        if response.status in (301, 307) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            yield redirected
        else:
            redirected = request.replace(
                url=redirected_url, method='GET', body=''
            )
            redirected.headers.pop('Content-Type', None)
            redirected.headers.pop('Content-Length', None)
            yield redirected
