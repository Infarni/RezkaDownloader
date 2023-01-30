#!/usr/bin/env python
import os
import sys
from threading import Thread
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from handlers import config, rezka_api, file_handler


def main():
    # Create data dir
    if not os.path.exists(config.PATH):
        os.mkdir(config.PATH)
    
    # Create web driver
    driver_options = Options()
    driver_options.add_argument('--disable-gpu')
    driver_options.add_argument('--log-level 3')
    driver_options.add_argument('--headless=new')
    driver_options.add_argument('--mute-audio')
    driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver_options.add_extension(os.path.join(config.PATH_EXTESIONS, 'Ublock_Origin.crx'))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver_options)
    
    # Main cycle
    while True:
        # Enter a url
        url = input('Enter a url: ')
        # Get to url
        driver.get(url)
        show_name = rezka_api.get_title(driver)
        print(f'\nShow name: {show_name}')
       
        # Get transtations
        translations = rezka_api.get_translations_list(driver)
        # Check translations exists
        if not translations is None:    
            print('\nTranslations:')
            for index, translate in enumerate(translations):
                print(f'{index + 1}. {translate}')
            # Choose transtation
            translate = translations[int(input('Enter a number translate: ')) - 1]
            rezka_api.choose_translate(driver, translations, translate)
        
        # Get seasons
        seasons = rezka_api.get_seasons_list(driver)
        # Check seasons exists
        if not seasons is None:
            show_path = os.path.join(config.PATH, show_name)
            # Check show dir exists
            if not os.path.exists(show_path):
                os.mkdir(show_path)

            print('\nSeasons:')
            for index, season in enumerate(seasons):
                print(f'{index + 1}. {season}')
            # Choose season
            season = seasons[int(input('Enter a number season: ')) - 1]
            rezka_api.choose_season(driver, seasons, season)
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
        rezka_api.choose_quality(driver, quality)
        
        # Get episodes
        episodes = rezka_api.get_episodes_list(driver)
        # Check episodes exists
        if not episodes is None:
            # Download video cycle
            for index, episode in enumerate(episodes):
                # Choose episode
                rezka_api.choose_episode(driver, episodes, episode)
                # Get video url
                video_url = rezka_api.get_video_url(driver)
                
                # Get video size
                video_size = file_handler.get_file_size(video_url)
                video_local_size = 0
                # Get file path
                filename = os.path.join(season_path, f'{episode}.mp4')
                # Create and run download thread
                thread = Thread(target=file_handler.download, args=(video_url, filename))
                thread.start()
                # Download progress-bar
                while video_size != video_local_size:
                    video_local_size = file_handler.get_local_file_size(filename)
                    print(f'Download video - {episode} ({video_local_size}/{video_size})', end='\r')
                    sleep(1)
                print(f'Download video - {episode} ({video_local_size}/{video_size})')
        else:
            video_url = rezka_api.get_video_url(driver)
                
            # Get video size
            video_size = file_handler.get_file_size(video_url)
            video_local_size = 0
            # Get file path
            filename = os.path.join(config.PATH, f'{show_name}.mp4')
            # Create and run download thread
            thread = Thread(target=file_handler.download, args=(file_handler, filename))
            thread.start()
            # Download progress-bar
            while video_size != video_local_size:
                video_local_size = file_handler.get_local_file_size(filename)
                print(f'Download video - {show_name} ({video_local_size}/{video_size})', end='\r')
                sleep(1)
            print(f'Download video - {show_name} ({video_local_size}/{video_size})')
        
        # Complete
        print('Complete!')


if __name__ == '__main__':
    main()
