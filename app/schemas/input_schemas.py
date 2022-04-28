from typing import Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    count: Optional[int] = Field(
        5,
        title='Count Posts',
        description='Number of posts on page',
        ge=1,
        le=200000,
    )
    page: Optional[int] = Field(
        1,
        title='Page number',
        description='Page number result for query',
        ge=1,
    )

    class Config:
        schema_extra = {'example': {'page': 1, 'count': 10}}


class SearchByTextInputModel(Pagination):
    text: str = Field(
        title='Search text',
        description='Поиск постов по тексту:  на выходе отдаются все посты, '
        'содержащие данный текст',
    )

    class Config:
        schema_extra = {
            'example': {
                **Pagination.Config.schema_extra['example'],  # type: ignore
                'text': 'добрый день',
            }
        }


class SearchByThread(Pagination):
    thread_id: int = Field(
        title='Search by thread id',
        description='Вывод постов заданной темы по topic_id',
    )

    class Config:
        schema_extra = {
            'example': {
                **Pagination.Config.schema_extra['example'],
                'thread_id': 88540,
            }
        }


class SearchByReplies(Pagination):
    post_id: int = Field(
        title='Search in related posts',
        description='Поиск по реплаям для данного post_id',
    )

    class Config:
        schema_extra = {'example': {'post_id': 11418049}}
