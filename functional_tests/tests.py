from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str) -> None:
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def enter_value_into_textbox(self, text: str):
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_for_a_single_user(self):
        # Edith has heard about a new online todolist app. She has gone
        # to checkout its homepage"
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id("id_new_item")
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
        self.browser.get(self.live_server_url)
        self.enter_value_into_textbox("Buy LG ultrafine display")
        self.wait_for_row_in_list_table("1: Buy LG ultrafine display")

        # She notices that her list has a unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Another user called Samuel visits the home page.

        # We use a new browser session to make sure that no information of Edith's is coming through cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page, there is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy LG ultrafine display", page_text)
        self.assertNotIn("mac mini", page_text)

        # Francis starts a new list bu entering a new item
        self.enter_value_into_textbox("Buy a new PS5")
        self.wait_for_row_in_list_table("1: Buy a new PS5")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no sign of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy LG ultrafine display", page_text)
        self.assertIn("Buy a new PS5", page_text)

        # Satisfied they both go back to sleep
