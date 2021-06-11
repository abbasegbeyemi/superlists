from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        _list = List.objects.create()
        response = self.client.get(f"/lists/{_list.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="Item 1", list=correct_list)
        Item.objects.create(text="Item 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="Other Item 1", list=other_list)
        Item.objects.create(text="Other Item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")
        self.assertNotContains(response, "Other Item 1")
        self.assertNotContains(response, "Other Item 2")


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        _list = List()
        _list.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = _list
        first_item.save()

        second_item = Item()
        second_item.text = "The second (ever) list item"
        second_item.list = _list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, _list)
        saved_items = Item.objects.all()

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, _list)
        self.assertEqual(second_saved_item.text, "The second (ever) list item")
        self.assertEqual(second_saved_item.list, _list)


class NewItemTest(TestCase):
    def test_can_save_a_post_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item", data={"item_text": "A new item for an existing list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/add_item",
                                    data={"item_text": "A new item for an existing list"})

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
