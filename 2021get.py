import re
import requests
import json
from bs4 import BeautifulSoup
from json import JSONEncoder
import numpy

class Result:
	def __init__(self, info: str) -> None:
		self.info = info
		self.build()

	def build(self) -> None:
		outcome = re.split('\(|\)|@|#|\^', self.info)

		self.home = {'Team': outcome[0]}
		self.home['Record'] = outcome[1]
		self.away = {'Team': outcome[3]}
		self.away['Record'] = outcome[4]
		self.home['Score'] = outcome[6]
		self.away['Score'] = outcome[7]

	def jsonify(self) -> str:
		return json.dumps(self, indent=4,cls=Encoder)

class Box:
	def __init__(self, gameUrl: str) -> None:
		self.url = gameUrl
		self.build()

	def build(self) -> None:
		page = get_parsed_page("https://www.baseball-reference.com/" + self.url)
		header = page.find("h1").text
		header = header.split(" at ")
		header[1] = header[1].split(" Box")

		score = page.findAll("div", {"class": "score"})

		self.home = header[1][0]
		self.away = header[0]

		self.homeScore = score[1].text
		self.awayScore = score[0].text

		homeRecord = score[1].parent.next_sibling.text
		awayRecord = score[0].parent.next_sibling.text

		if self.homeScore > self.awayScore:
			homeRecord = homeRecord.split('-')
			homeRecord[0] = int(homeRecord[0])
			homeRecord[0] -= 1
			awayRecord = awayRecord.split('-')
			awayRecord[1] = int(awayRecord[1])
			awayRecord[1] -= 1
		elif self.homeScore < self.awayScore:
			homeRecord = homeRecord.split('-')
			homeRecord[1] = int(homeRecord[1])
			homeRecord[1] -= 1
			awayRecord = awayRecord.split('-')
			awayRecord[0] = int(awayRecord[0])
			awayRecord[0] -= 1

		self.homeRecord = str(homeRecord[0]) + "-" + str(homeRecord[1])
		self.awayRecord = str(awayRecord[0]) + "-" + str(awayRecord[1])

	def jsonify(self) -> str:
		return json.dumps(self, indent=4,cls=Encoder)

def get_parsed_page(url: str) -> None:
	headers = {
		"referer": "https://baseball-reference.com",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
	}

	return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def get_url_list() -> list:
	page = get_parsed_page("https://www.baseball-reference.com/leagues/majors/2019-schedule.shtml")

	data = page.find("div", {'id': "all_8500011529"})
	data = data.findAll("em")

	games = []

	for item in data:
		games.append(item.find("a")['href'])

	return games

def write() -> None:
	urls = get_url_list()

	f = open("2019.txt", "a")

	for url in urls:
		bs = Box(url)

		f.write("%s(%s)@%s(%s)^%s#%s\n" % (bs.home, bs.homeRecord, bs.away, bs.awayRecord, bs.homeScore, bs.awayScore))

	f.close()

def read(year: str) -> list:
	f = open(year + ".txt", "r")
	data = f.read()
	data = data.split("\n")
	data = data[:len(data) - 1]

	scores = []

	for line in data:
		score = Result(line)
		scores.append(score)

	return scores

class Encoder(JSONEncoder):
	def default(self, o):
		return o.__dict__

def total_runs_std():
	outcomes = read("2019")

	runs = []

	for outcome in outcomes:
		runs.append(int(outcome.home['Score']) + int(outcome.away['Score']))
	
	runs_average = numpy.average(runs)
	runs_std = numpy.std(runs)

	print(f'Total Runs\n Average: {runs_average}\n Std: {runs_std}')

	return runs_std

def home_runs_std():
	outcomes = read("2019")

	runs = []

	for outcome in outcomes:
		runs.append(int(outcome.home['Score']))
	
	runs_average = numpy.average(runs)
	runs_std = numpy.std(runs)

	print(f'Home Team Runs\n Average: {runs_average}\n Std: {runs_std}')

	return runs_std

def away_runs_std():
	outcomes = read("2019")

	runs = []

	for outcome in outcomes:
		runs.append(int(outcome.away['Score']))
	
	runs_average = numpy.average(runs)
	runs_std = numpy.std(runs)

	print(f'Away Team Runs\n Average: {runs_average}\n Std: {runs_std}')

	return runs_std

if __name__ == "__main__":
	outcomes = read("2019")

	print(outcomes[100].jsonify())

	total_runs_std()
	home_runs_std()
	away_runs_std()
