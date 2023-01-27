from time import sleep

import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_translations_list(driver: selenium.webdriver.Chrome) -> list | None:
    '''
    Get translations name list
    '''
    unformat_translations = driver.find_elements(By.CLASS_NAME, 'b-translator__item')
    
    if len(unformat_translations) == 0:
        return None
    
    translations = []
    
    for translate in unformat_translations:
        translations.append(translate.text)
    
    return translations



def get_seasons_list(driver: selenium.webdriver.Chrome)-> list | None:
    '''
    Get seasons name list
    '''
    unformat_seasons = driver.find_elements(By.CLASS_NAME, 'b-simple_season__item')
    
    if len(unformat_seasons) == 0:
        return None
    
    seasons = []
    
    for season in unformat_seasons:
        seasons.append(season.text)
    
    return seasons


def get_episodes_list(driver: selenium.webdriver.Chrome) -> list | None:
    '''
    Get episodes name list
    '''
    unformat_episodes = driver.find_elements(By.CLASS_NAME, 'b-simple_episode__item')
    
    if len(unformat_episodes) == 0:
        return None
    
    episodes = []
    
    for episode in unformat_episodes:
        episodes.append(episode.text)
    
    return episodes


def get_video_url(driver: selenium.webdriver.Chrome) -> str:
    '''
    Get source video
    '''
    player_block = driver.find_element(By.ID, 'cdnplayer')
    player_block.click()
    sleep(1)

    while True:
        url = driver.execute_script('return window.performance.getEntries();')[-1]
        name = url['name']
        if name[-3:] == '.ts':
            player_block.click()
            return name[:name.find('.mp4') + 4]


def get_title(driver: selenium.webdriver.Chrome):
    '''
    Get show title
    '''
    return driver.find_element(By.CLASS_NAME, 'b-post__title').text


def choose_translate(
    driver: selenium.webdriver.Chrome,
    translations: list, 
    translate: str
) -> bool:
    '''
    Choose translate
    '''
    web_elements = driver.find_elements(By.CLASS_NAME, 'b-translator__item')
    
    for web_element in web_elements:
        if web_element.text == translate:
            web_element.click()
            return True
    
    return False


def choose_season(
    driver: selenium.webdriver.Chrome,
    seasons: list,
    season: str
) -> bool:
    '''
    Choose season
    '''
    web_elements = driver.find_elements(By.CLASS_NAME, 'b-simple_season__item')
    
    for web_element in web_elements:
        if web_element.text == season:
            web_element.click()
            return True
    
    return False


def choose_quality(
    driver: selenium.webdriver.Chrome,
    quality: str='1080p'
) -> bool:
    '''
    Choose quality
    '''
    player_block = driver.find_element(By.ID, 'cdnplayer')
    sleep(1)
    player_block.find_element(By.XPATH, '//*[@id="oframecdnplayer"]/pjsdiv[15]/pjsdiv[3]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="cdnplayer_settings"]/pjsdiv/pjsdiv[1]').click()
    sleep(1)
    qualitys = player_block.find_elements(By.CSS_SELECTOR, '#cdnplayer_settings > pjsdiv:nth-child(1) > pjsdiv')
    
    for el in qualitys:
        if el.text == quality:
            el.click()
            sleep(1)
            return True
    
    return False


def choose_episode(
    driver: selenium.webdriver.Chrome,
    episodes: list,
    episode: str,
) -> bool:
    '''
    Choose episode
    '''
    web_elements = driver.find_elements(By.CLASS_NAME, 'b-simple_episode__item')
    
    for web_element in web_elements:
        if web_element.text == episode:
            web_element.click()
            return True
    
    return False
