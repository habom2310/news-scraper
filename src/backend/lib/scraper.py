from src.backend.lib.config import WebConfig
from src.backend.lib.browser import Browser
from src.backend.lib.models import Article
from src.backend.lib.postgresql_client import PostgresClient
import src.backend.lib.utils as utils

from bs4 import BeautifulSoup
import logging
# import random

class Scraper():
    def __init__(self, webname):
        self.logger = logging.getLogger("scraper")
        self._browser = Browser(fast_load=False)
        self._web_config = WebConfig(webname)
        self._db = PostgresClient()
        
    def scraping_main_page(self):
        '''
        scraping category urls from main page
        '''
        source_html = self._browser.load_page(self._web_config.get_main_url())
        if not source_html:
            return None

        self.logger.info("[Scraper] Scraping categories and sub-categories ...")
        soup = BeautifulSoup(source_html, "html.parser")

        main_category_tag = self._web_config.get_main_category_tag()
        main_category_class = self._web_config.get_main_category_class()

        list_cat = soup.find_all(main_category_tag, class_=main_category_class)
        ret = []
        for i, cat in enumerate(list_cat):
            ret.append({"category_name": cat.text, "category_url": cat["href"]})
        ret = utils.validate_list_category_urls(ret)
        self.logger.info(f"[Scraper] Found  {len(ret)} categories.")

        return ret

    def scraping_category_page(self, url):
        source_html = self._browser.load_page(url)
        if not source_html:
            return None

        soup = BeautifulSoup(source_html, "html.parser")

        cat_post_tag = self._web_config.get_cat_post_tag()
        cat_post_class = self._web_config.get_cat_post_class()
        
        list_article = soup.find_all(cat_post_tag, class_=cat_post_class)
        list_article_url = []
        if len(list(list_article))>0:
            list_article_url = [a.find("a").get("href") for a in list_article]

        self.logger.info(f"[Scraper] Scraping from {url}: found {len(list_article)} articles")

        return list_article_url

    def scraping_article_page(self, url, use_selenium=True):
        self.logger.info(f"[Scraper] Scraping from {url}")
        source_html = self._browser.load_page(self._web_config.get_main_url() + url, use_selenium=False)
        if not source_html:
            return None

        soup = BeautifulSoup(source_html, "html.parser")

        article_title_tag = self._web_config.get_article_title_tag()
        article_title_class = self._web_config.get_article_title_class()

        # article_metadata_tag = self._web_config.get_article_metadata_tag()
        # article_metadata_class = self._web_config.get_article_metadata_class()
        
        article_metadata_author_tag = self._web_config.get_article_metadata_author_tag()
        article_metadata_author_class = self._web_config.get_article_metadata_author_class()

        article_metadata_datetime_tag = self._web_config.get_article_metadata_datetime_tag()
        article_metadata_datetime_class = self._web_config.get_article_metadata_datetime_class()

        article_text_tag = self._web_config.get_article_text_tag()
        article_text_class = self._web_config.get_article_text_class()

        title = ""
        if title_div := soup.find(article_title_tag, class_=article_title_class):
            title = title_div.text

        author_name = ""
        author_url = ""
        if author_div := soup.find(article_metadata_author_tag, article_metadata_author_class):
            author_name = author_div.text
            author_url = author_div.find("a")

        update_time = ""
        if time_div := soup.find(article_metadata_datetime_tag, class_=article_metadata_datetime_class):
            update_time = time_div.text
            update_time = utils.parse_datetime(update_time, self._web_config.get_webname())

        full_text = ""
        list_related_article_urls = []
        for p in soup.find_all(article_text_tag, class_=article_text_class):
            a_tags = p.find_all("a")
            for a in a_tags:
                list_related_article_urls.append(a['href'])
            full_text += p.text + "\n"

        ret = { "article_url":url,
                "title":title, 
                "author_name":author_name,
                "author_url":author_url,
                "update_time":update_time,
                "full_text":full_text,
                "related_articles":list_related_article_urls
                }

        return ret

    def scraping_process(self):
        self.logger.info("[Scraper] Start scraping process ...")
        if list_category := self.scraping_main_page():
            pass
        else:    
            return None

        for cat in list_category:
            cat_url = cat["category_url"]
            if list_article_url := self.scraping_category_page(self._web_config.get_main_url() + cat_url):
                pass
            else:
                continue

            for article_url in list_article_url:
                if utils.validate_article_url(article_url) == False:
                    continue

                if article := self.scraping_article_page(article_url):
                    new_article = Article(
                        # article_id=random.randint(0,100000),
                        href = article.get("article_url"),
                        title = article.get("title"),
                        date = article.get("update_time"),
                        newspaper = self._web_config.get_webname(),
                        author_id = article.get("author_id", ""),
                        author_fullname = article.get("author_name",""),
                        content=article.get("full_text","")
                    )

                    self._db.push_article(new_article)