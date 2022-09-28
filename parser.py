import logging
import collections
import requests
import bs4
import datetime
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kijiji')

ParseResult = collections.namedtuple('ParseResult', ('title', 'date', 'url_image'))


class Client:

    def __init__(self):
        self.seasion = requests.Session()
        self.seasion.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48',
            'Accept-Language': 'en',
        }
        self.result = []

    def load_page(self, page: int = None):
        url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
        res = self.seasion.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.search-item')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):

        url_block = block.select_one('a.title')
        if not url_block:
            logger.error('no url_block')
            return

        url = url_block.get('href')
        link = f'https://www.kijiji.ca{url}'
        if not url:
            logger.error('no href')
            return

        date_block = block.select_one('div.location')
        dates = date_block.find_all('span', 'date-posted')
        for date in dates:
            if date.text[0] == '<' or 'Yesterday':
                date = datetime.today().strftime('%d/%m/%Y')
            else:
                date = date.text
        if not date_block:
            logger.error('no date_block')
            return

        image_block = block.select_one('div.image')
        url_img = image_block.find_all('img')
        for img in url_img:
            img_url = img.attrs.get("data-src")
            if not img_url:
                continue

        self.result.append(ParseResult(
            title=link,
            date=date,
            url_image=img_url
        ))

        logger.debug('%s', link)
        logger.debug('-' * 100)
        return link, date, img_url

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Количество квартир {len(self.result)}')
        tuple_result = list(self.result)
        return tuple_result


parser = Client()
sheet = parser.run()


