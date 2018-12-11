from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SearchResultsViewTest(TestCase):
    def test_invalid_search_entry(self):
        """
        If there are no valid drinks for the input search entries, the results view should load and
        say so
        """
        response = self.client.get(reverse('results'), data={'ingredient': ['badingredient']})
        self.assertContains(response, "No matching drinks found for ingredients: badingredient")

    def test_valid_search_entry(self):
        """
        If there are drinks for the input search entries, there should be results within the context
        to display
        """
        response = self.client.get(reverse('results'), data={'ingredient': ['lemon']})
        self.assertTrue(response.context['drinkResults'] != [])

# class DetailViewTest(TestCase):
#     def test_drink_with_no_ingredients_in_list(self):

        
