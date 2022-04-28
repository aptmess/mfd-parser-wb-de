import scrapy as sp


class TopicItem(sp.Item):
    topic_id: int = sp.Field()
    topic_name: str = sp.Field()
    topic_url: str = sp.Field()
    topic_main_num_page: int = sp.Field()


class PostItem(sp.Item):
    post_id = sp.Field()
    post_url = sp.Field()
    post_text = sp.Field()
    post_created_at = sp.Field()
    post_rating = sp.Field()
    is_deleted = sp.Field()
    related_to = sp.Field()
    topic_id = sp.Field()
    author_id = sp.Field()


class AuthorItem(sp.Item):
    author_id = sp.Field()
    author_name = sp.Field()
