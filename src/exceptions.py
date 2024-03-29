TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'
BROKEN_URL = 'Возникла ошибка при загрузке страницы "{url}"'
RESPONSE_IS_NONE = 'Вернулся пустой response при запросе {url}'


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass
