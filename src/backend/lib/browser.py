from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random
import logging
import requests

class Browser:
    def __init__(self, timeout=60, fast_load=True):
        options = Options()
        # options.add_argument("--headless")
        profile= webdriver.FirefoxProfile()
        self.logger = logging.getLogger()

        if fast_load==True:
            profile.set_preference('permissions.default.stylesheet', 2)
            # Disable images
            profile.set_preference('permissions.default.image', 2)
            # Disable notification
            profile.set_preference('permissions.default.desktop-notification', 2)
            # Disable Flash
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    
        self._driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path="webdriver/geckodriver.exe")
        self._driver.set_page_load_timeout(timeout)

    def load_page(self, url, use_selenium=True, wait=5, entropy=3):
        # Function: load page with url
        # Input:
        # - wait: time waiting for page to load
        # - entropy: small random add to waiting time
        if use_selenium:
            wait = int(wait + random.random() * entropy)
            # self._driver.set_page_load_timeout(wait) # Set timeout frequently may raise errors
            self._driver.implicitly_wait(wait)

            self._has_error = False
            a= True
            #while a:
            try: 
                self._driver.get(url)
                return self._driver.page_source
            except:
                self.logger.exception("Time out")
                self._has_error = True
                return None
        else:
            try:
                self._request = requests.get(url)
                return self._request.content

            except:
                self.logger.exception("Time out")
                self._has_error = True
                return None

