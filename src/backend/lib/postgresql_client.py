from sqlalchemy import Integer, Text, create_engine
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from contextlib import contextmanager
import pandas as pd
import json

with open('src/backend/db_config.json') as f:
    dbconfig = json.load(f)

POSTGRES_USERNAME = dbconfig.get("POSTGRES_USERNAME", "")
POSTGRES_PASSWORD = dbconfig.get("POSTGRES_PASSWORD", "")
POSTGRES_HOST = dbconfig.get("POSTGRES_HOST", "")
POSTGRES_PORT = dbconfig.get("POSTGRES_PORT", "")
POSTGRES_DB = dbconfig.get("POSTGRES_DB", "")

Base = declarative_base()

class Postgres_Article(Base):
    __tablename__ = 'articles'
    # basic fields
    article_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    href = Column(String, nullable=False)
    publish_date = Column(Date)
    newspaper = Column(String)
    category = Column(String)
    author_id = Column(String)
    author_fullname = Column(String)
    content = Column(Text, nullable=False) # full content

    # analytic fields
    related_articles = Column(String)
    sentimental = Column(String)
    keywords = Column(String)

class PostgresClient():
    def __init__(self, POSTGRES_USERNAME=POSTGRES_USERNAME, POSTGRES_PASSWORD=POSTGRES_PASSWORD, POSTGRES_HOST=POSTGRES_HOST, POSTGRES_PORT=POSTGRES_PORT, POSTGRES_DB=POSTGRES_DB):
        self.db_string = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        self.engine = create_engine(self.db_string)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine) # create table if they not exist
        self.logger = logging.getLogger("scraper")
        self._existed_article_urls = self.get_all_article_urls()
        if len(self._existed_article_urls) > 0:
            self._has_existed_articles = True
        else:
            self._has_existed_articles = False

    @contextmanager
    def get_session(self):
        session = self.Session()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
    def push_article(self, article):
        if self._has_existed_articles:
            if article.get_href() in self._existed_article_urls:
                self.logger.info("[DB] Article already existed in DB")
                return False

        new_article = Postgres_Article(
            # article_id = article.get_id(),
            title = article.get_title(),
            href  = article.get_href(),
            publish_date = article.get_date(),
            newspaper = article.get_newspaper(),
            category = article.get_category(),
            author_id = article.get_author_id(),
            author_fullname = article.get_author_fullname(),
            content = article.get_content()
        )
        
        with self.get_session() as sess:
            sess.add(new_article)
            try:
                sess.commit()
                self.logger.info("[DB] article successfully saved")
                self._existed_article_urls.append(article.get_href())
                return True
            except Exception as e:
                self.logger.exception("[DB] commit error!")
                return False

    def get_sample_articles(self):
        with self.get_session() as sess:
            for article in sess.query(Postgres_Article):
                print(f"Title: {article.title}")
                print(f"Newpspaper: {article.newspaper}")
                print(f"Link: {article.href}")
                print(f"Publish date: {article.publish_date}")
                print(f"Author: {article.author_fullname}")
                print(f"Content: {article.content}")
                print()

                input("Press Enter to print next article !")
                print()
            
    def get_all_article_urls(self):
        with self.get_session() as sess:
            df = pd.read_sql(sess.query(Postgres_Article.href).statement, sess.bind)

        if len(df)>0:
            return list(df["href"])
        else:
            return []