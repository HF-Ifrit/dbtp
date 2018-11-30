from locust import HttpLocust, TaskSet, task
import resource, random

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

# limit on how many ingredients to test on results page. Randomly picked between range
count_min = 0
count_max = 10

class UserBehavior(TaskSet):

	def on_start(self):
		self.login()

	def login(self):
		response = self.client.get("/login/")
		csrftoken = response.cookies.get('csrftoken', '')
		self.client.post("/login/", {"csrfmiddlewaretoken": csrftoken, "username": "test1", "password": "accounttesting123"})
	
	def getIngredients(self):
		f = open('ingredients.txt', 'r')
		content = f.read().replace('\n', '')
		ingredients = [x.strip() for x in content.split(',')]
		f.close()

		return ingredients

	
	@task(100)
	def loadHomePage(self):
		self.client.get("/")


	@task(85)
	def runSearchPage(self):

		ingredients = self.getIngredients()
		ingredient_count = random.randint(count_min, count_max)

		sampleList = []


		for x in range(0, ingredient_count):
			sampleList.append(random.choice(ingredients))

		url = "/results?"

		for ingredient in sampleList:
			url += "ingredient=" + ingredient + "&"

		self.client.get(url)

	@task(75)
	def loadIngredientList(self):
		self.client.get("/account/ingredients")


class WebsiteUser(HttpLocust):
	task_set = UserBehavior
	min_wait = 5000
	max_wait = 9000
