import logging
from abc import ABC, abstractmethod
from datetime import datetime

from scrapy import Item
from scrapy.selector.unified import Selector
from w3lib.html import remove_tags

log = logging.getLogger(__name__)


class Transformer(ABC):
    def __init__(
        self,
        xpath: str,
        column_name: str,
        post: Selector,
        get_all: bool = False,
    ):
        self._column_name = column_name
        self._xpath = xpath
        self._xpath_value = (
            post.xpath(self._xpath).get()
            if not get_all
            else post.xpath(self._xpath).getall()
        )

    @abstractmethod
    def transform(self, input_data: Item) -> (Item, bool):
        raise NotImplementedError


class PostIDTransformer(Transformer):
    """
    column_name: post_id
    xpath: "table//button[@class='mfd-button-attention']/@data-id"
    """

    def transform(self, input_data: Item) -> (Item, bool):
        input_data[self._column_name] = int(self._xpath_value)
        return input_data, True if self._xpath_value is not None else False


class PostIsDeletedTransformer(Transformer):
    """
    column_name: is_post_deleted
    xpath: "table//div[@class='mfd-post-remark']/text()"
    """

    def transform(self, input_data: Item) -> (Item, bool):
        input_data[self._column_name] = (
            self._xpath_value is not None and 'удалено' in self._xpath_value
        )
        return input_data, True


class PostRating(Transformer):
    """
    column_name: post_rating
    xpath:
        div[@class='mfd-post-top'] +
        /div[@class='mfd-post-top-2'] +
        /span/text()
    """

    def transform(self, input_data: Item) -> (Item, bool):
        try:
            input_data[self._column_name] = (
                int(self._xpath_value) if self._xpath_value != '\xa0' else 0
            )
        except Exception as ex:
            input_data[self._column_name] = 0
        return input_data, True


class PostCreatedAt(Transformer):
    """
    column_name: post_created_at
    xpath:
        div[@class='mfd-post-top'] +
        /div[@class='mfd-post-top-1'] +
        /a[@class='mfd-post-link']/text()
    """

    def transform(self, input_data: Item) -> (Item, bool):
        datetime_object = datetime.strptime(self._xpath_value, '%d.%m.%Y %H:%M')
        input_data[self._column_name] = datetime_object
        return input_data, True


class PostText(Transformer):
    """
    column_name: post_text
    xpath:
        div[@class='mfd-post-top'] +
        /div[@class='mfd-post-top-1'] +
        /a[@class='mfd-post-link']/text()
    """

    def transform(self, input_data: Item) -> (Item, bool):
        input_data[self._column_name] = (
            remove_tags(self._xpath_value.replace('<br>', '\n'))
            if self._xpath_value is not None
            else ''
        )
        return input_data, True


class PostAnsweredPosts(Transformer):
    """
    column_name: answers_on_post_ids
    xpath:
        div[@class='mfd-post-top'] +
        /div[@class='mfd-post-top-1'] +
        /a[@class='mfd-post-link']/text()
    """

    def transform(self, input_data: Item) -> (Item, bool):
        print(self._xpath_value)
        input_data[self._column_name] = ', '.join(
            [i.rpartition('id=')[2] for i in self._xpath_value]
        )
        return input_data, True


class AuthorID(Transformer):
    """
    column_name: author_id
    xpath:
        div[@class='mfd-post-top'] +
        /div[@class='mfd-post-top-0'] +
        /@title
    """

    def transform(self, input_data: Item) -> (Item, bool):
        okay_result = True
        try:
            input_data[self._column_name] = int(
                self._xpath_value.rpartition('ID: ')[2]
            )

        except Exception as ex:
            okay_result = False
        return input_data, okay_result


class AuthorName(Transformer):
    """
    column_name: author_name
    xpath:
        div[@class='mfd-post-top'] +
        /div[@class='mfd-post-top-0'] +
        /@title
    """

    def transform(self, input_data: Item) -> (Item, bool):
        okay_result = True
        try:
            input_data[self._column_name] = remove_tags(self._xpath_value)
        except Exception as ex:
            okay_result = False
        return input_data, okay_result
