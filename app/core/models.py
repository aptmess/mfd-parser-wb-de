import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import func
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Topic(Base):
    __tablename__ = 'topics'
    topic_id = sa.Column(sa.Integer, primary_key=True)
    topic_name = sa.Column(sa.String, unique=True, nullable=False)
    topic_url = sa.Column(sa.String, unique=True, nullable=True)
    topic_main_num_page = sa.Column(sa.Integer)

    post = so.relationship('Post')

    def __repr__(self) -> str:
        return f'User {self.topic_name}, topic_id: {self.topic_id}'


class Author(Base):
    __tablename__ = 'authors'

    author_id = sa.Column(sa.Integer, primary_key=True)
    author_name = sa.Column(sa.String, unique=True, nullable=False)

    post = so.relationship('Post')


class Post(Base):
    __tablename__ = 'posts'

    post_id = sa.Column(sa.Integer, primary_key=True)
    post_url = sa.Column(sa.String)
    post_text = sa.Column(sa.String, nullable=True)
    post_created_at = sa.Column(sa.DateTime(timezone=True), default=func.now())
    post_rating = sa.Column(sa.Integer)
    is_deleted = sa.Column(sa.Boolean)
    related_to = sa.Column(sa.String)
    topic_id = sa.Column(sa.Integer)
    author_id = sa.Column(sa.Integer)

    topic = so.relationship('Topic')
    author = so.relationship('Author')

    __table_args__ = (
        sa.ForeignKeyConstraint(
            ('topic_id',), ['topics.topic_id'], name='Topic__topic_id_fk'
        ),
        sa.ForeignKeyConstraint(
            ('author_id',), ['authors.author_id'], name='Author__author_id_fk'
        ),
    )
