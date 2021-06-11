import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.host = "web"
        self.selenium = webdriver.Remote(
            command_executor=os.environ['SELENIUM_HOST'],
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"
        else:
            self.live_server_url = f'http://{os.environ.get("DJANGO_LIVE_TEST_SERVER_ADDRESS")}'
        super().setUp()

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def wait_for_row_in_list_table(self, row_text: str) -> None:
        start_time = time.time()
        while True:
            try:
                table = self.selenium.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def enter_value_into_textbox(self, text: str):
        inputbox = self.selenium.find_element_by_id("id_new_item")
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)
