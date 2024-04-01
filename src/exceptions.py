TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'
BROKEN_URL = 'Возникла ошибка при загрузке страницы "{url}"'
RESPONSE_IS_NONE = 'Вернулся пустой response при запросе {url}'
NOT_FOUND = 'Ничего не нашлось'
# UNEXPECTED_STATUS = (
#     '\nНесовпадение статусов:\n'
#     '{full_link}\n'
#     'Статус в карточке - {status_int}\n'
#     'Ожидаемые статусы - {status_ext}'
# )
# SUMM_ERROR = ('\n Ошибка в сумме:\n'
#               'Всего PEP: {total_pep_count}'
#               'Всего статусов из карточек: {sum_from_cards}')
# STATUS_ERROR = ('\nОшибочный статус в общем списке: {short_status}\n'
#                 'Строка PEP: {pep_line}')


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass
