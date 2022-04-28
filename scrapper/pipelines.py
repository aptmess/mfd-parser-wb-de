import logging
import typing as t

from itemadapter import ItemAdapter
from scrapy.spiders import Spider

from app.core.engine import engine, get_session
from app.core.models import Author, Base, Post, Topic
from scrapper.items import AuthorItem, PostItem, TopicItem

log = logging.getLogger(__name__)


class ScrapyMFDPipeline:
    metastore = {
        'author': {
            'id_name': 'author_id',
            'class': Author,
            'id_alchemy': Author.author_id,
        },
        'topic': {
            'id_name': 'topic_id',
            'class': Topic,
            'id_alchemy': Topic.topic_id,
        },
        'post': {
            'id_name': 'post_id',
            'class': Post,
            'id_alchemy': Post.post_id,
        },
    }

    def __init__(self) -> None:
        self.session = next(get_session())
        Base.metadata.create_all(engine)

    def process_item(
        self, item: t.Union[AuthorItem, PostItem, TopicItem], spider: Spider
    ) -> t.Union[AuthorItem, PostItem, TopicItem]:
        adapter = ItemAdapter(item)

        if isinstance(item, TopicItem):
            query_params = self.metastore['topic']
        elif isinstance(item, AuthorItem):
            query_params = self.metastore['author']
        else:
            query_params = self.metastore['post']

        items_id_seen = (
            self.session.query(query_params['id_alchemy'])
            .filter(
                query_params['id_alchemy'] == adapter[query_params['id_name']]
            )
            .all()
        )
        if not items_id_seen:
            self.session.add(query_params['class'](**adapter))
            self.session.commit()
        log.info(spider)
        return item
