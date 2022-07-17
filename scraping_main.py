from src.backend.lib.scraper import Scraper
import logging.config
import logging
import yaml

with open('src/backend/input/logging.yaml','r') as f:
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)
logger=logging.getLogger("scraper")
logger.info("Start scraping process ...")

scraper = Scraper("CNN")
scraper.scraping_process()
