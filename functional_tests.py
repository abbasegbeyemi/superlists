from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a new online todolist app. She has gone
        # to checkout its homepage"
        self.browser.get("http://localhost:8000")

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
        inputbox.send_keys("Buy LG ultrafine display")

        # When she hits enter, the page updates and now the page lists
        # "1: Buy LG Ultrafine Display" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table("1: Buy LG ultrafine display")

        # There is still a textbox inviting her to add another item. She enters
        # "Mount mac mini under desk"

        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Mount mac mini under desk")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table("1: Buy LG ultrafine display")
        self.check_for_row_in_list_table("2: Mount mac mini under desk")

        self.fail("Finish the test!")

        # The page updates again and both items now appear in her lists

        # She wonders if the site will remember her list. She notices that the
        # site has generated a unique URL for her. There is some explanatory text
        # to that effect.

        # She visits the URL and sees that her list is still there.

        # Satisfied, she goes back to sleep

