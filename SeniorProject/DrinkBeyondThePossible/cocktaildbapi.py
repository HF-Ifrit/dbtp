import requests as req
import json

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
        
        #Get all detailed information for each drink found that matches
        for drink in data['drinks']:
            id = drink['idDrink']
            detailResult = idApiCall(id)
            detailObj = DrinkDetail(detailResult['drinks'][0]) #Detailed info comes back as first item in the drinks JSON
            self.drinks.append(detailObj)


class DrinkDetail:
    """Representation of the drinks and their information"""
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
        self.ingredients = {k:v for (k,v) in drinkDict.items() if "strIngredient" in k}
        self.measurements = {k:v for (k,v) in drinkDict.items() if "strMeasure" in k}


def ingredientApiCall(ingredient):
    """Return a JSON object containing list of drink info dictionaries using the input ingredient"""
    resp = req.get(INGREDIENT_SEARCH_URL, {'i': ingredient})
    data = json.loads(resp.text)
    return data

def idApiCall(id):
    """Return a JSON object containing a detailed drink info dictionary using a specific drink id"""
    resp = req.get(ID_DETAIL_SEARCH_URL, {'i': id})
    data = json.loads(resp.text)
    return data

def searchMatchingDrinks(ingredient):
    """Returns a SearchResult containing drinks and their details that have ingredients matching the input"""
    returnedDrinks = ingredientApiCall(ingredient)
    result = SearchResult(returnedDrinks)
    return result