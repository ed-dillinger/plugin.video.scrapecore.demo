# -*- coding: utf-8 -*-

'''*
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*'''

from commoncore import kodi

@kodi.register('main')
def main():
	kodi.add_menu_item({"mode": "browse_menu", "media": "shows"}, {"title": "TV Shows"})
	kodi.add_menu_item({"mode": "browse_menu", "media": "movies"}, {"title": "Movies"})
	kodi.add_menu_item({"mode": "list_modules"}, {"title": "List Resource Modules"})
	kodi.eod()

@kodi.register('browse_menu')
def browse_menu():
	from scrapecore import scrapers
	services = scrapers.get_browsable_scrapers(kodi.args['media'])
	for service, name in services:
		kodi.add_menu_item({'mode': 'browse_service', "service": service, "media": kodi.args['media']}, {'title': "Browse: %s" % name}, icon='png')
	kodi.eod()

@kodi.register('browse_service')
def browse_service():
	from scrapecore import scrapers
	if kodi.args['media'] == 'shows':
		shows = scrapers.list_shows(kodi.args['service'])
		for show in shows:
			image = show['image'] if 'image' in show else ''
			kodi.add_menu_item({'mode': 'browse_show', "service": kodi.args['service'], "url": show['url']}, {'title': show['title']}, image=image)
	else:
		movies = scrapers.list_movies(kodi.args['service'])
		for movie in movies:
			image = movie['image'] if 'image' in movie else ''
			kodi.add_menu_item({'mode': 'play_direct', "service": kodi.args['service'], "url": movie['url']}, {'title': movie['title']}, image=image)
	kodi.eod()

@kodi.register('browse_show')
def browse_show():
	from scrapecore import scrapers
	episodes = scrapers.list_episodes(kodi.args['service'], kodi.args['url'])
	for episode in episodes:
		image = episode['image'] if 'image' in episode else ''
		kodi.add_video_item({'mode': 'play_direct', "service": kodi.args['service'], "raw_url": episode['url']}, {'title': episode['title']}, random_url=False, image=image)
	kodi.eod()

@kodi.register('list_modules')
def list_modules():
	from scrapecore import scrapecore
	for r in scrapecore.get_installed_resources():
		kodi.add_menu_item({'mode': 'void', }, {'title': r['name']}, icon='')
	kodi.eod()	

@kodi.register('play_direct')
def play_stream():
	from scrapecore import scrapers
	resolved_url = scrapers.get_scraper_by_name(kodi.args['service']).resolve_url(kodi.args['raw_url'])
	if resolved_url: kodi.play_stream(resolved_url)

kodi.run()
