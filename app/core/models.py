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


# class Film(Base):
#     __tablename__ = 'films'
#
#     movie_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     title = sa.Column(sa.String, unique=True, nullable=False)
#     year = sa.Column(sa.Integer, sa.CheckConstraint('year >= 1900'))
#
#     grades = so.relationship('Grade')
#     comments = so.relationship('Comment')
#
#     def __repr__(self) -> str:
#         return f'Film `{self.title}`, film_id: {self.movie_id}'
#
#
# class Grade(Base):
#     __tablename__ = 'grades'
#
#     user_id = sa.Column(sa.Integer, primary_key=True)
#     movie_id = sa.Column(sa.Integer, primary_key=True)
#     grade = sa.Column(
#         sa.Integer, sa.CheckConstraint('0 <= grade <= 10'), nullable=False
#     )
#
#     users = so.relationship('User')
#     films = so.relationship('Film')
#
#     __table_args__ = (
#         sa.ForeignKeyConstraint(
#             columns=('user_id',),
#             refcolumns=['users.user_id'],
#             name='User__camp_id_fk',
#         ),
#         sa.ForeignKeyConstraint(
#             ('movie_id',), ['films.movie_id'], name='Film__movie_id_fk'
#         ),
#     )
#
#     def __repr__(self) -> str:
#         return (
#             f'Grade {self.grade} from user '
#             f'{self.user_id} to film {self.movie_id}'
#         )
#
#
# class Comment(Base):
#     __tablename__ = 'comments'
#
#     comment_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     user_id = sa.Column(sa.Integer)
#     movie_id = sa.Column(sa.Integer)
#     comment_text = sa.Column(sa.String, nullable=False)
#     dt = sa.Column(sa.DateTime(timezone=True), default=func.now())
#
#     users = so.relationship('User')
#     films = so.relationship('Film')
#
#     __table_args__ = (
#         sa.ForeignKeyConstraint(
#             columns=('user_id',),
#             refcolumns=['users.user_id'],
#             name='User__camp_id_fk',
#         ),
#         sa.ForeignKeyConstraint(
#             ('movie_id',), ['films.movie_id'], name='Film__movie_id_fk'
#         ),
#     )
#
#     def __repr__(self) -> str:
#         return (
#             f'Comment {self.comment_id} '
#             f'from user {self.user_id} to film {self.movie_id}'
#         )
