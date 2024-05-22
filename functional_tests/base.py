from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        staging_server = os.environ.get('STAGING_SERVER')  
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            
    def tearDown(self) -> None:
        self.browser.quit()
        
    
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()            
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    