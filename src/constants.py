from pathlib import Path
from urllib.parse import urljoin

PEP_URL = 'https://peps.python.org/'
MAIN_DOC_URL = 'https://docs.python.org/3/'


BASE_DIR = Path(__file__).parent

DOWNLOAD_DOC_URL = urljoin(MAIN_DOC_URL, 'download.html')
DOWNLOADS_DIR = BASE_DIR / 'downloads'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
