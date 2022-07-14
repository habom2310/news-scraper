import pytz
from datetime import datetime
from utils import get_utc_now_date

class Article:
    def __init__(self, article_id, href, topic, date, newspaper, language, sapo, content, feature_image, avatar, author_id=None, author_fullname = '', tags=[]):
        self._id = article_id
        self._href = href
        self._topic = topic.strip()
        self._date = date  # date is stored in UTC timezone
        self._newspaper = newspaper
        self._creation_date = pytz.utc.localize(datetime.utcnow()) # set utc now time
        self._keywords = []
        self._author_id = author_id
        self._author_fullname = author_fullname
        self._tokenized = False
        self._language = language
        self._sapo = sapo.strip()
        self._content = content # content is a list of dict [{'type':'text', 'content':''}, {'type':'image', 'link':'url'}]
        self._feature_image = feature_image # feature_image is an array  [url]
        self._avatar = avatar
        self._tags = tags
    
    def get_id(self):
        return self._id

    def get_tags(self):
        return self._tags

    def get_author_fullname(self):
        return self._author_fullname

    def get_author_id(self):
        return self._author_id

    def get_avatar(self):
        return self._avatar


    def get_href(self):
        return self._href

    def get_date(self):
        if type(self._date) != bool:
            return self._date
        else:
            return get_utc_now_date()

    def get_topic(self):
        return self._topic

    def get_newspaper(self):
        return self._newspaper

    def get_category(self):
        return self._category

    def get_sapo(self):
        return self._sapo
    def get_content(self):
        return self._content