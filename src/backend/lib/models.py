import pytz
from datetime import datetime

class Article:
    def __init__(self, href, title, newspaper, content, date=None, category=None, author_id=None, author_fullname = '', tags=[]):
        # self._id = article_id
        self._title = title.strip()
        self._href = href
        self._date = date  # date is stored in UTC timezone
        self._newspaper = newspaper
        self._category = category
        self._author_id = author_id
        self._author_fullname = author_fullname
        self._content = content
    
    def get_id(self):
        return self._id
    
    def get_href(self):
        return self._href
    
    def get_title(self):
        return self._title
    
    def get_date(self):
        if self._date:
            return self._date
        else:
            return pytz.utc.localize(datetime.utcnow())
        
    def get_newspaper(self):
        return self._newspaper
        
    def get_author_id(self):
        return self._author_id
    
    def get_author_fullname(self):
        return self._author_fullname
    
    def get_content(self):
        return self._content
    
    def get_category(self):
        return self._category

# class Article_manager():
