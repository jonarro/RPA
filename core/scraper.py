
import csv
import os
import time
from typing import Dict, List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.const import *

load_dotenv()

def search_people(config: Dict[str, str]):
    keywords = config["keywords"]
    location = config["location"]

    FULL_NAME = f"{keywords}_{location}_{time.strftime('%Y%m%d-%H%M%S')}.csv"

    # Crear una instancia
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    # Logging into LinkedIn
    driver.get(LOGIN_URL)
    time.sleep(2)

    user = os.getenv("USERNAME_LINKEDIN")
    password = os.getenv("PASSWORD_LINKEDIN")

    username = driver.find_element(By.ID, "username")
    username.send_keys(user)

    pword = driver.find_element(By.ID, "password")
    pword.send_keys(password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Abrir la página de búsqueda
    search_url = "https://www.google.com"
    driver.get(search_url)

    # Esperar hasta que el campo de entrada de búsqueda esté presente en la página
    input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

    input_search.send_keys(f"site:linkedin.com/in/ AND {keywords} AND {location}")
    input_search.submit()

    # Esperar hasta que aparezca el elemento de resultados de búsqueda en la página
    results_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'rcnt')))

    #scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Obtener el código fuente de la página de resultados de búsqueda
    src = driver.page_source
    
    #pasear el html
    soup = BeautifulSoup(src, 'lxml')

    profiles = soup.find_all('div', class_='MjjYud')

    for profile in profiles:
        profile_linkedin_url = profile.find('a')['href']
        page = driver.get(profile_linkedin_url)
        time.sleep(1)
        
        # obtener el codigo de la pagina
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        #Obtener el ur de la imagen
        div = soup.find('div', class_='pv-top-card__non-self-photo-wrapper ml0')
        
        img = div.find('img')['src'] if div else "No hay imagen"
        nombre = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text.strip()
        description = soup.find('div', class_= 'text-body-medium break-words').text.strip()
        empresa_actual = soup.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline')
        print(empresa_actual)
        about = soup.find('div', class_='inline-show-more-text full-width')
        print(about)
        time.sleep(2)

        


    
    
   


def scrappProfiles(config: Dict[str, str]) -> DataFrame:
    """
    Extrae perfiles de LinkedIn y los guarda en un archivo CSV.

    Args:
        config (dict): Configuración con las palabras clave y número de páginas a rastrear.

    Returns:
        DataFrame: Datos de los perfiles en formato DataFrame.
    """
    num_of_pages = range(1, int(config["pages"]) + 1)
    keywords = config["keywords"].replace(" ", "%20")
    title = config["title"].replace(" ", "%20")
    location = [str(GEO_URN[i]) for i in config["location"]]
    location_string = '["' + '"%2C"'.join(location) + '"]'
    geo_url = location_string

    # Full name of csv file is created with keywords and timestamp
    FULL_NAME = f"{keywords}_{title}_{time.strftime('%Y%m%d-%H%M%S')}.csv"
    profile_csv = open(FULL_NAME, 'w', encoding='utf-8')
    writer = csv.writer(profile_csv)
    writer.writerow(CSV_HEADERS)

    # Creating an instance
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)

    # Logging into LinkedIn
    driver.get(LOGIN_URL)
    time.sleep(2)

    user = os.getenv("USERNAME_LINKEDIN")
    password = os.getenv("PASSWORD_LINKEDIN")

    username = driver.find_element(By.ID, "username")
    username.send_keys(user)

    pword = driver.find_element(By.ID, "password")
    pword.send_keys(password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    for page in num_of_pages:
        # Open the search page
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}&page={page}&title={title}&geoUrn={geo_url}"

        # Get the HTML source code
        src = get_html(search_url, driver)

        # Parse the profiles
        parsed_profiles = parse_profiles(src)

        # Write the parsed profiles to the CSV file
        writer.writerows(parsed_profiles)

    profile_csv.close()
    return createDF(FULL_NAME)


def scrapp_jobs(config: Dict[str, str]) -> DataFrame:
    keywords = config["keywords"].replace(" ", "%20")
    page = config["pages"]

    FULL_NAME = f"{keywords}_{time.strftime('%Y%m%d-%H%M%S')}.csv"
    profile_csv = open(FULL_NAME, 'w', encoding='utf-8')
    writer = csv.writer(profile_csv)
    writer.writerow(['Title', 'Company', 'Location', 'Apply'])

    for page in range(1, int(page) + 1):
        html = requests.get(f"https://www.linkedin.com/jobs/search/?keywords={keywords}")
        print(html.text)
        soup = BeautifulSoup(html.text, 'lxml')
        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        for job in jobs:
            job_title = job.find('h3', class_='base-search-card__title').text.strip()
            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find('span', class_='job-search-card__location').text.strip()
            job_link = job.find('a', class_='base-card__full-link')['href']

            writer.writerow([job_title, job_company, job_location, job_link])
    
    profile_csv.close()

    return createDF(FULL_NAME)

    



def get_html(url: str, driver: webdriver.Chrome) -> str:
    """
    Obtiene el código fuente HTML de una página web siempre y cuando se use selenium.

    Args:
        url (str): URL de la página web a obtener.
        driver (webdriver.Chrome): Instancia del controlador web.

    Returns:
        str: Código fuente HTML de la página web.
    """
    driver.get(url)
    time.sleep(5)
    src = driver.page_source
    return src

def parse_profiles(src: str) -> List[List[str]]:
    """
    Analiza el código fuente HTML y extrae la información de los perfiles.

    Args:
        src (str): Código fuente HTML de la página web.

    Returns:
        list: Lista de perfiles con su información.
    """
    soup = BeautifulSoup(src, 'lxml')
    profiles = soup.find_all('li', {'class': 'reusable-search__result-container'})
    parsed_profiles = []

    for profile in profiles:
        name = "usuario de LinkedIn"
        occupation = profile.find('div', class_='entity-result__primary-subtitle t-14 t-black t-normal').text.strip()
        location = profile.find('div', class_='entity-result__secondary-subtitle t-14 t-normal').text.strip()
        url = profile.find('a', class_='app-aware-link')['href']
        img = profile.find('img')
        img = img['src'] if img is not None else "no hay imagen"
        info_extra = profile.find('p', class_='entity-result__summary entity-result__summary--2-lines t-12 t-black--light')
        info_extra = info_extra.text.strip() if info_extra is not None else "no hay información extra"
        parsed_profiles.append([name, occupation, location, url, img, info_extra])

    return parsed_profiles


def createDF(csv_file: str) -> DataFrame:
    """
    Crea un DataFrame con los datos de un archivo CSV.

    Args:
        csv_file (str): Ruta del archivo CSV.

    Returns:
        DataFrame: Datos del archivo CSV en formato DataFrame.
    """
    df = pd.read_csv(csv_file)
    return df