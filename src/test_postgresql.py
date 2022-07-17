# UNIT TEST
import numpy as np
from src.backend.lib.models import Article
from backend.lib.postgresql_client import PostgresClient
import json
import datetime

with open('src/backend/db_config.json') as f:
    dbconfig = json.load(f)

POSTGRES_USERNAME = dbconfig.get("POSTGRES_USERNAME", "")
POSTGRES_PASSWORD = dbconfig.get("POSTGRES_PASSWORD", "")
POSTGRES_HOST = dbconfig.get("POSTGRES_HOST", "")
POSTGRES_PORT = dbconfig.get("POSTGRES_PORT", "")
POSTGRES_DB = dbconfig.get("POSTGRES_DB", "")

# sample_article = Article(
#     article_id = np.random.randint(0, 1000000),
#     href = 'https://test.com',
#     title = 'day la bai test 2',
#     date = datetime.datetime.now(),
#     newspaper = 'CNN',
#     author_id = '100',
#     author_fullname = 'Ha Nguyen',
#     content = """
#     xcvxsdfsdfsfsdfsdf
#     sdfsdf
#     sdf
#     """
# )
# print("Test push a sample article")
db = PostgresClient(POSTGRES_USERNAME,POSTGRES_PASSWORD,POSTGRES_HOST,POSTGRES_PORT,POSTGRES_DB)
# db.push_article(sample_article)
# print("OK")
# print("Test list articles in database")
db.get_sample_articles()
print("OK")