import os
from time import sleep

import requests
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Rezka(selenium.webdriver.Chrome):
    url = 'https://rezka.ag'


    def __init__(self, path_to_extension: str):
        self_options = Options()
        self_options.add_argument('--disable-gpu')
        self_options.add_argument('--log-level 3')
        self_options.add_argument('--headless=new')
        self_options.add_argument('--mute-audio')
        self_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self_options.add_extension(path_to_extension)
        
        super().__init__(options=self_options)
        
        self.get(self.url)
    
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'url':
            if self.url != 'https://rezka.ag':
                self.get(value)
                self.get_title()
                self.update_translations_list()
                self.update_seasons_list()
                self.update_episodes_list()
                self.__quality = '480p'




    def update_translations_list(self) -> list:
        '''
        Get translations name list
        '''
        unformat_translations = self.find_elements(By.CLASS_NAME, 'b-translator__item')
        
        if len(unformat_translations) == 0:
            return []
        
        translations = []
        
        for translate in unformat_translations:
            translations.append(translate.text)
        
        self.__translations_list = translations
        self.__translation = translations[0]
        return translations



    def update_seasons_list(self) -> list:
        '''
        Get seasons name list
        '''
        unformat_seasons = self.find_elements(By.CLASS_NAME, 'b-simple_season__item')
        
        if len(unformat_seasons) == 0:
            return []
        
        seasons = []
        
        for season in unformat_seasons:
            seasons.append(season.text)
        
        self.__seasons_list = seasons
        self.__season = seasons[0]
        return seasons


    def update_episodes_list(self) -> list:
        '''
        Get episodes name list
        '''
        episodes_lists = self.find_elements(By.CLASS_NAME, 'b-simple_episodes__list')
        
        unformat_episodes = []
        for episodes_list in episodes_lists:
            if episodes_list.get_attribute('style') != 'display: none;':
                unformat_episodes = episodes_list.find_elements(By.CLASS_NAME, 'b-simple_episode__item')
        
        if len(unformat_episodes) == 0:
            return [self.__title]

        episodes = []
        
        for episode in unformat_episodes:
            episodes.append(episode.text)
        
        self.__episodes_list = episodes
        self.__episode = episodes[0]
        return episodes


    def choose_translate(
        self,
        translate: str
    ) -> None:
        '''
        Choose translate
        '''
        web_elements = self.find_elements(By.CLASS_NAME, 'b-translator__item')
        
        for web_element in web_elements:
            if web_element.text == translate:
                web_element.click()
                sleep(1)
                break
        
        self.__translation = translate
        self.update_seasons_list()


    def choose_season(
        self,
        season: str
    ) -> None:
        '''
        Choose season
        '''
        web_elements = self.find_elements(By.CLASS_NAME, 'b-simple_season__item')
        
        for web_element in web_elements:
            if web_element.text == season:
                web_element.click()
                sleep(1)
                break
        
        self.__season = season
        self.update_episodes_list()


    def choose_quality(
        self,
        quality: str='480p'
    ) -> None:
        '''
        Choose quality
        '''
        if quality not in ['1080p', '720p', '480p', '360p']:
            return

        if quality != '480p':
            player_block = self.find_element(By.ID, 'cdnplayer')
            sleep(1)
            player_block.find_element(By.XPATH, '//*[@id="oframecdnplayer"]/pjsdiv[15]/pjsdiv[3]').click()
            sleep(1)
            self.find_element(By.XPATH, '//*[@id="cdnplayer_settings"]/pjsdiv/pjsdiv[1]').click()
            sleep(1)
            qualitys = player_block.find_elements(By.CSS_SELECTOR, '#cdnplayer_settings > pjsdiv:nth-child(1) > pjsdiv')
            
            for el in qualitys:
                if el.text == quality:
                    el.click()
                    sleep(1)
                    break
        
        self.__quality = quality


    def choose_episode(
        self,
        episode: str,
    ) -> None:
        '''
        Choose episode
        '''
        episodes_lists = self.find_elements(By.CLASS_NAME, 'b-simple_episodes__list')
        
        for episodes_list in episodes_lists:
            if episodes_list.get_attribute('style') != 'display: none;':
                web_elements = episodes_list.find_elements(By.CLASS_NAME, 'b-simple_episode__item')
        
        for web_element in web_elements:
            if web_element.text == episode:
                web_element.click()
                sleep(1)
                break
        
        self.__episode = episode


    def get_title(self, update=False) -> str:
        '''
        Get show title
        '''
        title = self.find_element(By.CLASS_NAME, 'b-post__title').text
        self.__title = title
        return title


    def get_search_result(self, request: str) -> list:
        '''
        Get shows list
        '''
        search_field = self.find_element(By.ID, 'search-field')
        search_field.send_keys(request)
        search_field.send_keys(Keys.RETURN)
        
        unformat_shows = self.find_elements(By.CLASS_NAME, 'b-content__inline_item-cover')
        
        if len(unformat_shows) == 0:
            return []
        
        shows = []
        
        for show in unformat_shows:
            url = show.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            title = show.find_element(By.CSS_SELECTOR, 'a > img').get_attribute('alt')
            img = show.find_element(By.CSS_SELECTOR, 'a > img').get_attribute('src')
            shows.append(
                {
                    'name': title,
                    'url': url,
                    'img': img
                }
            )
        
        return shows


    def get_video_urls(self, start: int=0, end: int=-1, first=False) -> list:
        '''
        Get source video
        '''
        urls = []
        title = self.get_title()
        
        player_block = self.find_element(By.ID, 'cdnplayer')
        
        if first:
            player_block.click()
            
            self.execute_script('window.performance.clearResourceTimings();')
            sleep(1)
            while True:
                url = self.execute_script('return window.performance.getEntries();')[-1]
                name = url['name']
                if name[-3:] == '.ts':
                    player_block.click()
                    return [{'name': title, 'url': name[:name.find('.mp4') + 4]}]
        
        if end == -1:
            episodes_list = self.__episodes_list[start:]
        
        for episode in episodes_list:
            self.choose_episode(episode)
            player_block.click()

            self.execute_script('window.performance.clearResourceTimings();')
            while True:
                url = self.execute_script('return window.performance.getEntries();')[-1]
                name = url['name']
                if name[-3:] == '.ts':
                    player_block.click()
                    urls.append({'name': episode, 'url': name[:name.find('.mp4') + 4]})
                    break
        
        return urls
