from Config_Templates import Templates
from time import sleep
from os import path
import os
import re
import csv
import sys
import json
import requests
import datetime
import logging

# Configures Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(lineno)s %(funcName)s %(message)s")
file_handler = logging.FileHandler('output.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Driver:
	def __init__(self):
		self.templates = Templates()
		
		self.userInput()
		self.mainDriver()

	def userInput(self):
		search_query = list()
		limits = list()
		special_keywords = list()

		print("\t\tALL INPUT FIELDS SHOULD BE ,(COMMA) SEPARATED")

		while True : 
			search_query = [ item.strip().replace(' ','+') for item in input("Enter search queries: \n").split(',') ]
			limits = list(map( int ,[item.strip() for item in input("Enter corresponding max limits: \n").split(",")] ))
			special_keywords = [ item.strip() for item in input("Enter corresponding keywords to look for: \n").split(",") ]

			if ((len(search_query) == len(limits) == len(special_keywords)) and len(search_query)) :
				self.search_query = tuple(search_query)
				self.limits = tuple(limits)
				self.special_keywords = tuple(special_keywords)
				break
			else :
				print("wrong input", end="\r");sleep(1)
				print("try again  ")

	def mainDriver(self):

		if not path.isdir("cache"):
			os.mkdir("cache")

		for query in range(len(self.search_query)):
			print(f"Running for {self.search_query[query]}")
			
			self.saveSearchPage(self.search_query[query], self.limits[query])
			print(f"\tGot search results")
			
			self.channelIdFromSearch(self.limits[query])
			print(f"\tGot all channels")

			self.channelVideoPage()
			print(f"\tGot Channel Video Pages")

	def saveSearchPage(self, search, limit):

		self.saved_search_page = path.join("cache", search)

		if not path.isfile(self.saved_search_page):
			with open(self.saved_search_page, 'a+') as search_page:
				search_query_result = requests.get(self.templates.search_base + search)
				search_page.write(search_query_result.text)
			logger.info(f"Saved search for {search}")
		else:
			logger.info(f"{search} already exists")

	def channelIdFromSearch(self, limit):
		
		channel_ids = set()
		self.channel_ids = set()
		self.channel_subs = set()

		with open(self.saved_search_page) as file:
			for line in file:
				channel_ids.update(re.finditer(self.templates.channel_id_on_searchpage, line))
		
		channel_ids = set(list(channel_ids)[:limit])
		for channel in channel_ids:
			if (channel.group(1) != self.templates.black_list):
				video_page = self.templates.channel_base + channel.group(1) + "/videos"
				video_page_source = requests.get(video_page)
				subs_count = re.search(self.templates.channel_subs, video_page_source.text).group(1,2)
				
				if float(subs_count[0]) >= 1 :
					with open(path.join("cache", channel.group(1)), "w") as file:
						file.write(video_page_source.text)

					self.channel_ids.add(channel.group(1))
					self.channel_subs.add(subs_count)
		print(list(zip(self.channel_ids, self.channel_subs)))
					


	def channelVideoPage(self):
		pass	


a = Driver()