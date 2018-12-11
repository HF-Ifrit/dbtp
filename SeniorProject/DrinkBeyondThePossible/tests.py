from django.test import TestCase
from django.urls import reverse
from . import cocktaildbapi

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


class CocktailDBAPITest(TestCase):
    def test_drink_detail_creation(self):
        drinkDict = {
            'idDrink': '111',
            'strDrink': 'TestDrink',
            'strVideo': None,
            'strCateogry': 'Fruity',
            'strIBA': 'N/A',
            'strAlcoholic': 'Alcoholic',
            'strGlass': 'Highball',
            'strInstructions': 'Mix ingredients',
            'strDrinkThumb': None,
            'strIngredient1': 'Ing1',
            'strIngredient2': 'Ing2',
            'strMeasure1': 'Little',
            'strMeasure2': 'A lot'
        }
        
        detail = cocktaildbapi.DrinkDetail(drinkDict)

        self.asserEquals(detail.__repr__(), "DrinkDetail(111,TestDrink)")
        self.assertEquals(detail.ingredients, ['Ing1','Ing2'])
        self.assertEquals(detail.measurements, ['Little', 'A lot'])
    
    def test_drink_detail_creation(self):
        drinkDict = {
            'idDrink': '111',
            'strDrink': 'TestDrink',
            'strVideo': None,
            'strCategory': 'Fruity',
            'strIBA': 'N/A',
            'strAlcoholic': 'Alcoholic',
            'strGlass': 'Highball',
            'strInstructions': 'Mix ingredients',
            'strDrinkThumb': None,
            'strIngredient1': 'Ing1',
            'strIngredient2': 'Ing2',
            'strMeasure1': 'Little',
            'strMeasure2': 'A lot'
        }

        same1 = cocktaildbapi.DrinkDetail(drinkDict)
        same2 = cocktaildbapi.DrinkDetail(drinkDict)

        self.assertTrue(same1.__eq__(same2))

        differentDict = drinkDict
        differentDict['idDrink'] = '222'
        different = cocktaildbapi.DrinkDetail(differentDict)

        self.assertFalse(same1.__eq__(different))
