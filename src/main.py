import logging
import re
from urllib.parse import urljoin
from collections import Counter
import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import (
    BASE_DIR, MAIN_DOC_URL,
    WHATS_NEW_URL, PEP_URL, EXPECTED_STATUS)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def pep(session):
    """Парсер информации из статей о нововведениях в Python."""

    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, 'lxml')

    num_index = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(num_index, 'tbody')
    tr_tags = tbody_tag.find_all('tr')

    total_pep_count = 0
    status_counter = Counter()

    results = [('Статус', 'Количество')]

    for pep_line in tqdm(tr_tags):
        total_pep_count += 1
        short_status = pep_line.find('td').text[1:]
        try:
            status_ext = EXPECTED_STATUS[short_status]
        except KeyError:
            status_ext = []
            logging.info(
                f'\nОшибочный статус в общем списке: {short_status}\n'
                f'Строка PEP: {pep_line}'
            )

        link = find_tag(pep_line, 'a')['href']
        full_link = urljoin(PEP_URL, link)
        response = get_response(session, full_link)
        soup = BeautifulSoup(response.text, 'lxml')
        dl_tag = find_tag(soup, 'dl')
        status_line = dl_tag.find(string='Status')

        if not status_line:
            logging.error(f'{full_link} - не найдена строка статуса')
            continue
        status_line = status_line.find_parent()
        status_int = status_line.next_sibling.next_sibling.string
        if status_int not in status_ext:
            logging.info(
                '\nНесовпадение статусов:\n'
                f'{full_link}\n'
                f'Статус в карточке - {status_int}\n'
                f'Ожидаемые статусы - {status_ext}'
            )
        status_counter[status_int] += 1

    results.extend(status_counter.items())
    sum_from_cards = sum(status_counter.values())

    if total_pep_count != sum_from_cards:
        logging.error(
            f'\n Ошибка в сумме:\n'
            f'Всего PEP: {total_pep_count}'
            f'Всего статусов из карточек: {sum_from_cards}'
        )
        results.append(('Total', sum_from_cards))
    else:
        results.append(('Total', total_pep_count))
    return results


def whats_new(session):
    """Парсер информации из статей о нововведениях в Python."""

    response = get_response(session, WHATS_NEW_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(WHATS_NEW_URL, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
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
        raise Exception('Ничего не нашлось')

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
    FILE = r'.+pdf-a4\.zip$'
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    table_tag = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a',
                          {'href': re.compile(FILE)})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
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
