from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a new online todolist app. She has gone
        # to checkout its homepage"
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists.
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish the test!")

        # She is invited to enter a to-do item straight away

        # She types "LG ultrafine display" into a text box

        # When she hits enter, the page updates and now the page lists
        # "1: Buy LG Ultrafine Display" as an item in a to-do list

        # There is still a textbox inviting her to add another item. She enters
        # "Mount mac mini under desk"

        # The page updates again and both items now appear in her lists

        # She wonders if the site will remember her list. She notices that the
        # site has generated a unique URL for her. There is some explanatory text
        # to that effect.

        # She visits the URL and sees that her list is still there.

        # Satisfied, she goes back to sleep
