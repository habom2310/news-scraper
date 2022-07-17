import pytz
from datetime import datetime
import yaml
import logging
import re

#logging
# logging.basicConfig(filename="scraping.log",
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.INFO)

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger().setLevel(logging.INFO)

# fileHandler = logging.FileHandler("scraping.log",mode="a")
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

logger = logging.getLogger("scraper")

def get_utc_now_date():
    return pytz.utc.localize(datetime.utcnow())

def load_config_file(file_path):
    with open(file_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            logger.exception("yaml error")


# craper utils
def validate_article_url(url):
    valid = True
    if "http" in url:
        valid = False
        
    if "/video/" in url:
        valid = False
        
    if "/videos/" in url:
        valid = False
        
    if "/live-news/" in url:
        valid = False

    if "/gallery/" in url: # only has pictures
        valid = False
        
    return valid

def validate_list_category_urls(list_category):
    '''
    list_category=[{"category_name": "world", "category_url": "/world"}, ...]
    '''
    list_urls = []
    valid_list_category = []
    for cat in list_category:
        if cat["category_url"] not in list_urls:
            list_urls.append(cat["category_url"])
            valid_list_category.append(cat)

    return valid_list_category


def parse_datetime(to_be_parsed, webname):
    if webname == "CNN":
        # Updated 0615 GMT (1415 HKT) July 16, 2022
        t = re.compile("(\d{4})").search(to_be_parsed).span()
        str_t = to_be_parsed[t[0]:t[1]]
        str_t = str_t[:2] + ":" + str_t[2:]
        d = re.compile("([a-z]{1,10} \d{1,2}, \d{4})").search(to_be_parsed.lower()).span()
        str_d = to_be_parsed[d[0]:d[1]]

        datetime_object = datetime.strptime(f"{str_d} {str_t}", '%B %d, %Y %H:%M')
        return datetime_object

