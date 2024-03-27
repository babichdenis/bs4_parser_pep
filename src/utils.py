import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import (
    BROKEN_URL,
    TAG_NOT_FOUND, ParserFindTagException
)


def get_response(session, url):
    """Перехват ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            BROKEN_URL.format(url=url),
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Поиск тега в супе и перехват исключения если тег не найден"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        logging.error(
            TAG_NOT_FOUND.format(tag=tag, attrs=attrs), stack_info=True
        )
        raise ParserFindTagException(
            TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return searched_tag
