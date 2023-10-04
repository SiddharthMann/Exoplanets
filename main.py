import time
import csv 
import requests
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

START_URL = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

planet_data = []
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

def scraping ():
    for i in range (1, 221):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,'html.parser')
            currentPage= int (soup.find_all('input', attrs={'class', 'page_num'})[0].get('value'))

            if currentPage <i:
                browser.find_element(By.XPATH, value = '//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            elif currentPage >i:
                browser.find_element(By.XPATH, value = '//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
            else:
                break
        
        for ul_tag in soup.find_all('ul', attrs={'class', 'exoplanet'}):
            li_tags= ul_tag.find_all('li')
            temp= []
            for index, li_tag in enumerate(li_tags):
                if index == 0 :
                    temp.append(li_tag.find_all('a')[0].contents[0])
                else:
                    try:
                        temp.append(li_tag.contents[0])

                    except:
                        temp.append('')
            hyperlink=li_tags[0]
            temp.append("https://exoplanets.nasa.gov"+ hyperlink.find_all("a", href=True)[0]["href"])
            planet_data.append(temp)
        
        browser.find_element(By.XPATH, value = '//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(f'page {i} scraping completed')    

scraping()

new_planet_data = []
def scrapemoredata(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content, 'html.parser')
        temp= []
        for tr_tag in soup.find_all('tr', attrs={'class': 'fact_row'}):
            td_tags=tr_tag.find_all('td')
            for td_tag in td_tags :
                try:
                    temp.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp.append('')
        
        new_planet_data.append(temp)
    except:
        time.sleep(1)
        scrapemoredata(hyperlink)
    
for index, data in enumerate(planet_data):
    scrapemoredata(data[5])

print(new_planet_data[0:5])

final_planet_data = []
for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+ new_planet_data)

with open("final.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)