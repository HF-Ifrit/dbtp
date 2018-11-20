import json
from multiprocessing import pool

import requests as req

INGREDIENT_SEARCH_URL = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?'
"""Format of results in returned JSON: {strDrink, strDrinkThumb, idDrink}"""

ID_DETAIL_SEARCH_URL = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?'
"""Format of results in returned JSON (some entries omitted): 
{idDrink, strDrink, strVideo, strCategory, strIBA, strAlcoholic, strGlass, strInstructions, strDrinkThumb, 
strIngredient1...2...3..etc, strMeasure1...2...3..etc}
"""


class SearchResult:
    """Representation of the JSON object list received from the ingredient search api call"""

    def __init__(self, data):
        self.drinks = []
        
        # TODO: Build SearchResult using parallelism
        # Get all detailed information for each drink found that matches
        drink_ids = [drink['idDrink'] for drink in data]
        with pool.Pool(processes=10) as p:
            self.drinks = p.map(self.build_result, data)

    def build_result(self, drink_id):
        detailResult = idApiCall(drink_id)
        detailObj = DrinkDetail(detailResult)
        return detailObj


class DrinkDetail:
    """Representation of the drinks and their information"""

    __IGNORED__ = [' ', '\n', '', None]

    def __init__(self, drinkDict):
        self.id = drinkDict['idDrink']
        self.name = drinkDict['strDrink']
        self.video = drinkDict['strVideo']
        self.category = drinkDict['strCategory']
        self.iba = drinkDict['strIBA']
        self.alcoholic = drinkDict['strAlcoholic']
        self.glass = drinkDict['strGlass']
        self.instructions = drinkDict['strInstructions']
        self.thumbimage = drinkDict['strDrinkThumb']

        self.ingredients = [v for (k, v) in drinkDict.items(
        ) if "strIngredient" in k and v not in DrinkDetail.__IGNORED__]
        self.measurements = [v for (k, v) in drinkDict.items(
        ) if "strMeasure" in k and v not in DrinkDetail.__IGNORED__]

    def __eq__(self, other):
        if isinstance(other, DrinkDetail):
            return self.id == other.id

    def __repr__(self):
        return "DrinkDetail({},{})".format(self.id, self.name)

    def __hash__(self):
        return hash(self.__repr__())


def ingredientApiCall(ingredient):
    """Return a JSON object containing list of drink info dictionaries containing name, ID, and image using the input ingredient"""
    resp = req.get(INGREDIENT_SEARCH_URL, params={'i': ingredient})
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return None
    else:
        return data['drinks']


def idApiCall(id):
    """Return a JSON object containing a detailed drink info dictionary using a specific drink id"""
    resp = req.get(ID_DETAIL_SEARCH_URL, params={'i': id})
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return None
    else:
        return data['drinks'][0]


def searchMatchingDrinks(ingredient):
    """Returns a SearchResult containing drinks and their details that have ingredients matching the input"""
    returned_drinks = ingredientApiCall(ingredient)

    return SearchResult(returned_drinks) if returned_drinks is not None else None


def find_matching_drinks(ingredient_list):
    matching = []
    for ingredient in ingredient_list:
        matching.append(searchMatchingDrinks(ingredient))

    return matching


def find_recommended_drinks(ingredient_list):
    similar = {}

    for ingredient in ingredient_list:
        drinks = ingredientApiCall(ingredient)
        for drink in drinks:
            if drink['idDrink'] not in similar:
                similar[drink['idDrink']] = drink

    return list(similar.values())


def get_drink_details(drink_id):
    json_details = idApiCall(drink_id)
    details = DrinkDetail(json_details)

    return details