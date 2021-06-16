from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit an empty list item.
        # She hits enter on an empty listbox

        # Home page refreshes and there is an error message sayig the input box cannot be blank.
        self.wait_for(
            lambda: self.assertEqual(
                self.selenium.find_element_by_css_selector(".has-error").text,
                "You can't have an empty list item")
        )
        # She tries again with some text which now works.

        # She then tries again with another empty imput box and gets a similar error

        # She can correct it by filling some text in

        # self.fail("Write me!")
