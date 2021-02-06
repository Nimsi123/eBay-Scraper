from scraper_api import ScraperAPIClient
import pandas as pd
from Ebay.ItemOrganization.timer import timer

"""
SOME STATS
fast_download is hitting roughly 130 api requests every 10 minutes.

Threads | Average API Request time

5  | 2.4
10 | 1.4
15 | 1.1
20 | 1.4

Timing before
?

"""

class Client:

	api_keys = [
		'bfb3cb210e50c39d09f82432095a5150', #nimarahmanian2020@gmail.com
		'cbbdd094d7401d8912b09341e37be9b1', #nimarahmanian8@gmail.com
		'c733663048589db82005534b6739c32e', #nimsi@berkeley.edu
		'10c2e4d0fef8e45470a5b43b84f15ec0', #oxaxe7@gmail.com
		'81d0339948cd0596cf05a03df5b32288', #rahmanian.arya2356@gmail.com
		'042d872c6185752c4b3db850014bace1', #nikolas-cacerces
		"7b3ed1376b2358ebf50609d891ace0b4", #nimarahmanianstorage1@gmail.com
	]

	csv_file = "..\\..\\Ebay\\ItemOrganization\\Client.csv"
	df = pd.read_csv(csv_file)
	
	current_index = 2
	current_client = ScraperAPIClient( api_keys[current_index] )
	counter = df["counter"][current_index]
	counter_limit = 1000

	def next_client():
		"""Once an api key has run out of free requests, switch clients. 
		Increments Client.current_index, updates Client.current_client, and initializes Client.counter."""

		Client.current_index += 1
		if Client.current_index == len(Client.api_keys):
			print("ran out of api requests.")
			import sys
			sys.exit()

		Client.current_client = ScraperAPIClient( Client.api_keys[Client.current_index] )
		Client.counter = Client.df["counter"][Client.current_index]

	def update_counter():
		"""Increments Client.counter and updates .csv file"""
		Client.counter += 1
		df = pd.read_csv(Client.csv_file)
		df.at[Client.current_index, "counter"] = Client.counter
		df.to_csv(Client.csv_file, index = False)

	@timer
	def get(url):
		"""Essentially a wrapper function to client.get(url). If the counter exceedes the counter_limit, use the next available client.

		:param url: Downloads the HTML at the url.
		:type url: str
		:returns: The page's HTML
		:rtype: requests.models.Response
		"""

		print("{0:30}: {1}\n".format("CLIENT COUNTER", Client.counter))

		if Client.counter >= Client.counter_limit:
			Client.next_client()

		Client.update_counter()
		return Client.current_client.get(url)

	""" 	Miscellaneous 	"""
	def print_usage():
		"""Prints the usage data for every account associated with an API key."""
		for key in Client.api_keys:
			client = ScraperAPIClient(key)
			print(client.account())

	def reset_csv():
		"""Updates Client.csv with the requestCount number for each api key. 
		This method should be called a minute after the last API call."""

		data = [(key, ScraperAPIClient(key).account()["requestCount"]) for key in Client.api_keys]

		df_api_keys = pd.DataFrame(data, columns= ["api_key", "counter"])
		df_api_keys.to_csv( Client.csv_file )
