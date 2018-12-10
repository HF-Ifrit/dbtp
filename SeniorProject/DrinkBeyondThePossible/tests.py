from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SearchResultsViewTest(TestCase):
    def test_no_search_results(self):
        """
        If there are no valid drinks for the input search entries, the results view should load and
        say so
        """
        response = self.client.post(reverse('results'), data={'ingredient': ['badIngredient']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.text, "No matching drinks found for ingredients: badIngredient ")
