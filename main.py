#!/usr/bin/env python
import os
import sys
from threading import Thread
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from handlers import config, rezka, file_handler


def main():
    # Create data dir
    if not os.path.exists(config.PATH):
        os.mkdir(config.PATH)
    
    # Create web driver
    driver = rezka.Rezka()
    
    # Main cycle
    while True:
        # Enter a url
        url = input('Enter a url: ')
        # Get to url
        driver.url = url
        show_name = driver.get_title()
        print(f'\nShow name: {show_name}')
       
        # Get transtations
        translations = driver.update_translations_list()
        # Check translations exists
        if len(translations) != 0:    
            print('\nTranslations:')
            for index, translate in enumerate(translations):
                print(f'{index + 1}. {translate}')
            # Choose transtation
            translate = translations[int(input('Enter a number translate: ')) - 1]
            driver.choose_translate(translate)
        
        # Get seasons
        seasons = driver.update_seasons_list()
        # Check seasons exists
        if len(seasons) != 0:
            show_path = os.path.join(config.PATH, show_name)
            # Check show dir exists
            if not os.path.exists(show_path):
                os.mkdir(show_path)

            print('\nSeasons:')
            for index, season in enumerate(seasons):
                print(f'{index + 1}. {season}')
            # Choose season
            season = seasons[int(input('Enter a number season: ')) - 1]
            driver.choose_season(season)
            season_path = os.path.join(show_path, season)
            # Check season dir exists
            if not os.path.exists(season_path):
                os.mkdir(season_path)
        
        # Qualitys list
        qualitys = ['1080p', '720p', '480p', '360p']
        print('\nQualitys:')
        for index, quality in enumerate(qualitys):
            print(f'{index + 1}. {quality}')
        # Choose quality
        quality = qualitys[int(input('Enter a number quality: ')) - 1]
        driver.choose_quality(quality)
        
        # Get episodes
        episodes = driver.update_episodes_list()

        # Download video cycle
        for index, episode in enumerate(episodes):
            if episode != show_name:
                # Choose episode
                driver.choose_episode(episode)
                # Get file path
                filename = os.path.join(season_path, f'{episode}.mp4')
            else:
                # Get file path
                filename = os.path.join(config.PATH, f'{episode}.mp4')

            # Get video url
            video = driver.get_video_urls(first=True)[0]
            
            # Get video size
            video_size = file_handler.get_file_size(video['url'])
            video_local_size = 0
            
            # Create and run download thread
            thread = Thread(target=file_handler.download, args=(video['url'], filename))
            thread.start()
            # Download progress-bar
            while video_size != video_local_size:
                video_local_size = file_handler.get_local_file_size(filename)
                print(f'''Download video - {video['name']} ({video_local_size}/{video_size})''', end='\r')
                sleep(1)
            print(f'''Download video - {video['name']} ({video_local_size}/{video_size})''')


if __name__ == '__main__':
    main()
