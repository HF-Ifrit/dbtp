from locust import HttpLocust, TaskSet, task
import resource, random

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

ingredients = []


class UserBehavior(TaskSet):

	def on_start(self):
		self.login()
		self.getIngredients()

	# may not be needed, main parts to stress test are home and search results
	def login(self):
		response = self.client.get("/login/")
		csrftoken = response.cookies.get('csrftoken', '')
		self.client.post("/login/", {"csrfmiddlewaretoken": csrftoken, "username": "test1", "password": "accounttesting123"})
	
	def getIngredients(self):
		f = open('ingredients.txt', 'r')
		content = f.read().replace('\n', '')
		ingredients = [x.strip() for x in content.split(',')]

	
	@task(100)
	def loadHomePage(self):
		self.client.get("/")


	@task(85)
	def runSearchPage(self):
		count_min = 0
		count_max = 10

		ingredient_count = random.randint(count_min, count_max)

		sampleList = []

		for x in range(0, ingredient_count):
			pick = random.randint(0, len(ingredients) + 1) - 1
			sampleList.append(ingredients[pick])

		# TODO, use sample list to make post call on get drinks view
		

	@task(75)
	def loadIngredientList(self):
		self.client.get("/account/ingredients")


class WebsiteUser(HttpLocust):
	task_set = UserBehavior
	min_wait = 5000
	max_wait = 9000
