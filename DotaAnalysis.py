import requests
import json
from bs4 import BeautifulSoup

def sanitize(input):
	col_count = 0
	clean_str = ""
	for i in str(input):
		if col_count == 2 and i != "]":
			clean_str = clean_str + i
		elif col_count == 2 and i == "]":
			break
		if i == ":":
			col_count = col_count + 1

	return clean_str

dota_heroes = requests.get("https://api.opendota.com/api/heroes/")

dota_heroes = json.loads(dota_heroes.content)

steam_id = input("Please enter steam ID: ")
url_to_scrape = "https://steamidfinder.com/lookup/" + steam_id

r = requests.get(url_to_scrape)

site_HTML = r.text

souped_site = BeautifulSoup(site_HTML, "html.parser")

#search for all <code></code> blocks in html script
codes = souped_site.find_all("code")

#take steamID3 and trim to only include id tag
player_id = sanitize(codes[3])

#gets basic player data from open dota
response = requests.get(" https://api.opendota.com/api/players/ " + player_id)

#convert json data to a dictionary
player_dat = json.loads(response.content)
profile = player_dat['profile']

print(str(profile['personaname']) + ": " + str(player_dat['solo_competitive_rank']))

params = {'hero_id': 8}

player_heroes = requests.get("https://api.opendota.com/api/players/"+ player_id +"/heroes/")

heroes = json.loads(player_heroes.content)

best_heroes = []
hero_info = []

#print(heroes)
#for x in heroes:
#	print(x)


for x in heroes:
	win = x['win']
	games = x['games']
	hero_id = x['hero_id']

	if int(games) > 0:
		win_rate = int(win)/int(games)
	else:
		win_rate = 0

	#len(dota_heroes) = 115

	if int(hero_id) != 119 and int(hero_id) != 120:
		temp = dota_heroes[int(hero_id) -1]
		name = temp['localized_name']
	if int(hero_id) == 119:
		temp = dota_heroes[113]
		name = temp['localized_name']
	if int(hero_id) == 120:
		temp = dota_heroes[114]
		name = temp['localized_name']

	#print(str(name) + ": " + str(win_rate) + "     " + str(games))

	if win_rate > .53 and games > 15:
		hero_info.clear()
		if int(hero_id) != 119 and int(hero_id) != 120:
			hero = dota_heroes[int(hero_id) -1]
		if int(hero_id) == 119:
			hero = dota_heroes[113]
		if int(hero_id) == 120:
			hero = dota_heroes[114]

		hero_info.append(hero_id)
		hero_info.append(hero['localized_name'])
		hero_info.append(win_rate)
		print(hero_info)
		#best_heroes.append(hero_info)

#print(best_heroes)