import os
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

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
        super(NewVisitorTest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(NewVisitorTest, self).tearDown()

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

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.selenium.get(self.live_server_url)
        self.selenium.set_window_size(1024, 768)

        # She notices that the input box is nicely centered
        inputbox = self.selenium.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )

        # She starts a new list and sees tha the input is nicely centered there too
        self.enter_value_into_textbox("testing")
        self.wait_for_row_in_list_table("1: testing")

        inputbox = self.selenium.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10
        )

    def test_can_start_a_list_for_a_single_user(self):
        # Edith has heard about a new online todolist app. She has gone
        # to checkout its homepage"
        self.selenium.get(self.live_server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn("To-Do", self.selenium.title)
        header_text = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.selenium.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            'Enter a to-do item'
        )

        # She types "Buy LG Ultrafine Display" into a text box
        # When she hits enter, the page updates and now the page lists
        # "1: Buy LG Ultrafine Display" as an item in a to-do list
        self.enter_value_into_textbox("Buy LG ultrafine display")
        self.wait_for_row_in_list_table("1: Buy LG ultrafine display")

        # There is still a textbox inviting her to add another item. She enters
        # "Mount mac mini under desk"

        self.enter_value_into_textbox("Mount mac mini under desk")

        # The page updates again and both items now appear in her lists
        self.wait_for_row_in_list_table("1: Buy LG ultrafine display")
        self.wait_for_row_in_list_table("2: Mount mac mini under desk")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.selenium.get(self.live_server_url)
        self.enter_value_into_textbox("Buy LG ultrafine display")
        self.wait_for_row_in_list_table("1: Buy LG ultrafine display")

        # She notices that her list has a unique url
        edith_list_url = self.selenium.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Another user called Samuel visits the home page.

        # We use a new selenium session to make sure that no information of Edith's is coming through cookies etc
        self.selenium.quit()
        self.selenium = webdriver.Remote(
            command_executor=os.environ['SELENIUM_HOST'],
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )

        # Francis visits the home page, there is no sign of Edith's list
        self.selenium.get(self.live_server_url)
        page_text = self.selenium.find_element_by_tag_name("body").text
        self.assertNotIn("Buy LG ultrafine display", page_text)
        self.assertNotIn("mac mini", page_text)

        # Francis starts a new list bu entering a new item
        self.enter_value_into_textbox("Buy a new PS5")
        self.wait_for_row_in_list_table("1: Buy a new PS5")

        # Francis gets his own unique URL
        francis_list_url = self.selenium.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no sign of Edith's list
        page_text = self.selenium.find_element_by_tag_name("body").text
        self.assertNotIn("Buy LG ultrafine display", page_text)
        self.assertIn("Buy a new PS5", page_text)

        # Satisfied they both go back to sleep

    @skip
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit an empty list item.
        # She hits enter on an empty listbox

        # Home page refreshes and there is an error message sayig the input box cannot be blank.

        # She tries again with some text which now works.

        # She then tries again with another empty imput box and gets a similar error

        # She can correct it by filling some text in

        self.fail("Write me!")
