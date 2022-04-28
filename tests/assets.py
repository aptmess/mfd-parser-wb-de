import datetime

from app.core.models import Author, Post, Topic

AUTHORS = [
    Author(author_id=user_id, author_name=f'user_{user_id}')
    for user_id in range(1, 5)
]

TOPICS = [
    Topic(
        topic_id=topic_id,
        topic_name=f'topic_name_{topic_id}',
        topic_main_num_page=0,
    )
    for topic_id in range(1, 5)
]

POSTS_DICT = {
    1: dict(
        post_id=1,
        post_url='',
        post_text='привет саша',
        post_rating=1,
        post_created_at=datetime.datetime(2022, 4, 10, 10, 0, 0),
        is_deleted=False,
        related_to='',
        topic_id=1,
        author_id=1,
    ),
    2: dict(
        post_id=2,
        post_url='',
        post_text='привет еще раз',
        post_rating=-1,
        post_created_at=datetime.datetime(2022, 4, 13, 11, 0, 0),
        is_deleted=False,
        related_to='1',
        topic_id=1,
        author_id=2,
    ),
    3: dict(
        post_id=3,
        post_url='',
        post_text='интересный день сегодня!',
        post_rating=0,
        post_created_at=datetime.datetime(2022, 4, 11, 10, 0, 0),
        is_deleted=False,
        related_to='',
        topic_id=2,
        author_id=3,
    ),
    4: dict(
        post_id=4,
        post_url='',
        post_text='ты мне не нравишься',
        post_rating=-1,
        post_created_at=datetime.datetime(2022, 4, 11, 11, 0, 0),
        is_deleted=False,
        related_to='3',
        topic_id=2,
        author_id=4,
    ),
    5: dict(
        post_id=5,
        post_url='',
        post_text='ты мне тоже',
        post_rating=1,
        post_created_at=datetime.datetime(2022, 4, 11, 12, 0, 0),
        is_deleted=False,
        related_to='4',
        topic_id=2,
        author_id=3,
    ),
}

POSTS = [Post(**post) for post in POSTS_DICT.values()]
