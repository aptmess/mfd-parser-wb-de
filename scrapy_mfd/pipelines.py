from itemadapter import ItemAdapter

from app.core.engine import engine, get_session
from app.core.models import Author, Base, Post, Topic
from scrapy_mfd.items import AuthorItem, PostItem, TopicItem


class ScrapyMFDPipeline:
    def __init__(self):
        self.session = next(get_session())
        Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if isinstance(item, TopicItem):
            items_id_seen = (
                self.session.query(Topic.topic_id)
                .filter(Topic.topic_id == adapter['topic_id'])
                .all()
            )
            if not items_id_seen:
                self.session.add(Topic(**adapter))
                self.session.commit()
        elif isinstance(item, AuthorItem):
            author_seen = (
                self.session.query(Author.author_id)
                .filter(Author.author_id == adapter['author_id'])
                .all()
            )
            if not author_seen:
                print('HERE', adapter['author_id'])
                self.session.add(Author(**adapter))
                self.session.commit()
        elif isinstance(item, PostItem):
            post_seen = (
                self.session.query(Post.post_id)
                .filter(Post.post_id == adapter['post_id'])
                .all()
            )
            if not post_seen:
                self.session.add(Post(**adapter))
                self.session.commit()

        return item

    # def close_spider(self, spider):
    #     self.session.close()
