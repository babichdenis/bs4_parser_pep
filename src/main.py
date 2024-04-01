import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOAD_DOC_URL, EXPECTED_STATUS,
                       MAIN_DOC_URL, PEP_URL, WHATS_NEW_URL)
from exceptions import NOT_FOUND, ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response


def pep(session):
    """Парсер информации из статей о нововведениях в Python."""
    response = get_response(session, PEP_URL)
    if response is None:
        return None

    soup = BeautifulSoup(response.text, features='lxml')
    pep_table = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    pep_table_data = find_tag(pep_table, 'tbody')
    pep_tags = pep_table_data.find_all('tr')
    errors = []
    result = [('Статус', 'Количество')]
    status_sum = defaultdict(int)
    error_messages = []

    for pep_tag in tqdm(pep_tags):
        pep_abbr = find_tag(pep_tag, 'abbr')
        preview_status = pep_abbr.text[1:]
        href = find_tag(pep_tag, 'a')['href']
        pep_link = urljoin(PEP_URL, href)
        response = get_response(session, pep_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        description = find_tag(
            soup, 'dl', attrs={'class': 'rfc2822 field-list simple'})
        td = description.find(string='Status')
        status = td.find_parent().find_next_sibling().text

        try:
            if status not in EXPECTED_STATUS[preview_status]:
                errors.append((pep_link, preview_status, status))
                error_message = (f'Несовпадающие статусы:\n'
                                 f'Статус в карточке: {status}\n'
                                 f'Ожидаемые статусы:'
                                 f' {EXPECTED_STATUS[preview_status]}')
                error_messages.append(error_message)
        except KeyError:
            logging.error('Непредвиденный код статуса в превью: '
                          f'{preview_status}')

        status_sum[status] += 1

    logging.warning('\n'.join(error_messages))

    result.extend(status_sum.items())
    result.append(('Total', sum(status_sum.values())))
    return result


def whats_new(session):
    """Парсер информации из статей о нововведениях в Python."""

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    response = get_response(session, WHATS_NEW_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    if not sections_by_python:
        raise ParserFindTagException(NOT_FOUND)
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag["href"]
        version_link = urljoin(WHATS_NEW_URL, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    """Парсер статусов версий Python."""

    REG_EX = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    ul_tags = soup.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException(NOT_FOUND)

    results = [('Ссылка на докуметацию', 'Версия', 'Статус')]
    pattern_r = REG_EX
    for a_tag in a_tags:
        text_match = re.search(pattern_r, a_tag.text)
        link = a_tag['href']
        if text_match:
            version = text_match.group(1)
            status = text_match.group(2)
        else:
            version = a_tag.text
            status = ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    """Скачивает архив с документацией"""

    FILE = r'.+pdf-a4\.zip$'

    response = get_response(session, DOWNLOAD_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    table_tag = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a',
                          {'href': re.compile(FILE)})
    pdf_a4_link = pdf_a4_tag['href']

    archive_url = urljoin(DOWNLOAD_DOC_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR = BASE_DIR / 'downloads'
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранен: {archive_path}')


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception:
        logging.exception('Ошибка при выполнении.', stack_info=True)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
