# %%
import os
import time
from typing import Dict, List,Any

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.const import *

load_dotenv()

# %%
def init_cli():
    mjs = """
    _________.__              .__  .__  __  .__        ___________.__
    ____________________  _____       _____  __________________________   
    \______   \______   \/  _  \     /     \ \_   _____|__    ___/  _  \  
     |       _/|     ___/  /_\  \   /  \ /  \ |    __)_  |    | /  /_\  \ 
     |    |   \|    |  /    |    \ /    Y    \|        \ |    |/    |    \\
     |____|_  /|____|  \____|__  / \____|__  /_______  / |____|\____|__  /
            \/                 \/          \/        \/                \/ 
   """
    print(mjs)

# %%
def get_one_profile(driver,curren_url: str):
    # obtener el codigo de la pagina
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    #Obtener el ur de la imagen
    div = soup.find('div', class_='pv-top-card__non-self-photo-wrapper ml0')
    img = div.find('img')['src'] if div else "No hay imagen"
    nombre = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words')
    nombre = nombre.text.strip() if nombre else "No hay nombre"
    description = soup.find('div', class_= 'text-body-medium break-words')
    description = description.text.strip() if description else "No hay descripcion"
    empresa_actual = soup.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline')
    empresa_actual = empresa_actual.text.strip() if empresa_actual else "No hay empresa actual"
    about = soup.find('section', class_='artdeco-card ember-view relative break-words pb3 mt2')
    if about:
      about = about.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width')
      about = about.text.strip() if about else "No hay about"
      about = about.replace("… ver más", "")
    
    experiencias = soup.find_all('div',class_="pvs-list__outer-container")
    
    exp = [{
    "puesto": experiencia.find('div', class_='display-flex align-items-center mr1 t-bold').text.strip() if experiencia.find('div', class_='display-flex align-items-center mr1 t-bold') else "No hay puesto",
    "img": experiencia.find('img')['src'] if experiencia.find('img') else "No hay imagen",
    "empresa": experiencia.find('span', class_='t-14 t-normal').text.strip() if experiencia.find('span', class_='t-14 t-normal') else "No hay empresa",
    "fecha": experiencia.find('span', class_='t-14 t-normal t-black--lightl').text.strip() if experiencia.find('span', class_='t-14 t-normal t-black--lightl') else "No hay fecha"
    }
    for experiencia in experiencias
      if experiencia.find('div', class_='display-flex align-items-center mr1 t-bold') and experiencia.find('div', class_='display-flex align-items-center mr1 t-bold').text.strip() != "No hay puesto"
    ]
    conocimientos_aptitudes = soup.find_all('div', class_='pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns')
    conocimiento = [{
      "nombre": conocimiento_aptitud.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold').text.strip() if conocimiento_aptitud.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold') else "No hay nombre",
      "descripcion": conocimiento_aptitud.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width').text.strip() if conocimiento_aptitud.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width') else "No hay descripcion",
    }
    for conocimiento_aptitud in conocimientos_aptitudes
    ]
    info_idiomas = soup.find_all('section', class_='artdeco-card ember-view relative break-words pb3 mt2')
    info_idiomas = [idioma for idioma in info_idiomas if idioma.find('div', id='languages')]
    idiomas = []
    for idioma in info_idiomas:
        items = idioma.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for item in items:
            nombre_idioma = item.find('div', class_='display-flex align-items-center mr1 t-bold').text.strip() if item.find('div', class_='display-flex align-items-center mr1 t-bold') else "No hay idioma"
            nivel = item.find('span', class_='t-14 t-normal t-black--light').text.strip() if item.find('span', class_='t-14 t-normal t-black--light') else "No hay nivel"
            idioma_data = {
                "idioma": nombre_idioma,
                "nivel": nivel
            }
            idiomas.append(idioma_data)
    educaciones = soup.find_all('section', class_='artdeco-card ember-view relative break-words pb3 mt2')
    educaciones = [edu for edu in educaciones if edu.find('div', id='education')]
    educacion = []
    for edu in educaciones:
        items = edu.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for item in items:
            img = item.find('img')['src'] if item.find('img') else "No hay imagen"
            escuela = item.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold').text.strip() if item.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold') else "No hay nombre"
            especialidad = item.find('span', class_='t-14 t-normal').text.strip() if item.find('span', class_='pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal') else "No hay especialidad"
            educacion_data = {
                "img": img,
                "escuela": escuela,
                "especialidad": especialidad
            }
            
            educacion.append(educacion_data)
  
    licencias_certificaciones = soup.find_all('section', class_='artdeco-card ember-view relative break-words pb3 mt2')
    licencias = []
    for licencia in licencias_certificaciones:
        if licencia.find('div', id='licenses_and_certifications'):
            items = licencia.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
            for item in items:
                img = item.find('img')['src'] if item.find('img') else "No hay imagen"
                nombre = item.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold').text.strip() if item.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold') else "No hay nombre"
                plataforma = item.find('span', class_='t-14 t-normal').text.strip() if item.find('span', class_='t-14 t-normal') else "No hay plataforma"
                expedicion = item.find('span', class_='t-14 t-normal t-black--light').text.strip() if item.find('span', class_='t-14 t-normal t-black--light') else "No hay expedicion"
                URL_certificacion = item.find('a')['href'] if item.find('a') else "No hay URL"
                licencia_data = {
                    "img": img,
                    "nombre": nombre,
                    "plataforma": plataforma,
                    "expedicion": expedicion,
                    "URL_certificacion": URL_certificacion
                }
                licencias.append(licencia_data)
    info = {
       "URL": curren_url,
        "nombre": nombre,
        "img": img,
        "description": description,
        "empresa_actual": empresa_actual,
        "about": about if about else "No hay about",
        "idiomas": idiomas if idiomas else "No hay idiomas",
        "experiencias": exp if exp else "No hay experiencias",
        "conocimientos_aptitudes" : conocimiento if conocimiento else "No hay conocimientos y aptitudes",
        "educacion": educacion if educacion else "No hay educacion",
        "licencias_certificaciones": licencias if licencias else "No hay licencias y certificaciones"
    }
    return info

# %%
def scrap_data_from_profile(driver,urls_profiles: List[str]):
  data_profiles = []
  for url in urls_profiles:
      driver.get(url)
      try:
         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pv-top-card--list')))
      except Exception as e:
        print(e)
        print(f"Error en {url}")
        time.sleep(5)
        continue
      #ir hasta abajo de la pagina
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(5)
      data_profiles.append(get_one_profile(driver,url))
  return data_profiles

# %%

def search_by_keyword(driver,config: Dict[str, str],urls_profiles: List[str]):
      global user_id
      keywords = config["keyword"]
      location = config["location"]
      initial_page = config["initial_page"]
      final_page = config["final_page"]
    # Abrir la página de búsqueda
      search_url = "https://www.google.com"
      driver.get(search_url)
       # Esperar hasta que el campo de entrada de búsqueda esté presente en la página
      input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

      input_search.send_keys(f"site:linkedin.com/in/ AND {keywords} AND {location}")
      input_search.submit()

      for _ in range(final_page):
             # Esperar hasta que aparezca el elemento de resultados de búsqueda en la página
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'rcnt')))

              # Obtener el código fuente de la página de resultados de búsqueda
        src = driver.page_source

              #pasear el html
        soup = BeautifulSoup(src, 'lxml')

        profiles = soup.find_all('div', class_='MjjYud')

        for profile in profiles:
          profile_linkedin_url = profile.find('a')['href']
          try:
            if profile_linkedin_url.startswith('/search'):
              break
            urls_profiles.append(profile_linkedin_url)
          except Exception as e:
            insert_error({
            "timestamp": format_timestamp(time.time()),
            "state": "scrapping",
            "error_message": "error al obtener el url del perfil",
            "request_url": search_url,
            "stack_trace": str(e),
            "additional_info": "profile_linkedin_url",
            "user_id": user_id,})
            continue
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
          next_button = driver.find_element(By.ID, 'pnnext')
          next_button.click()
        except Exception as e:
          print(e)
          print(urls_profiles)
          continue
      print(f"Se obtuvieron {len(urls_profiles)} urls de perfiles")
      info = scrap_data_from_profile(driver, urls_profiles)
      df = pd.DataFrame(info)
      return df

# %%
def is_logged(driver):
    #ver si hay un elemento con la clase form__input--text input_verification_pin
    try:
        driver.find_element(By.CLASS_NAME, 'form__input--text input_verification_pin')
        return True
    except Exception:
        return False

# %%

def insert_error(error):
  headers = {
    'Content-Type': 'application/json',
  }
  j = json.dumps(error)
  return requests.post("http://localhost:8787/error", data=j, headers=headers).json()

# %%
def search_by_urls(driver,urls_profiles: List[str]):
    info = scrap_data_from_profile(driver, urls_profiles)
    df = pd.DataFrame(info)
    return df

# %%
from datetime import datetime
def format_timestamp(timestamp: float) -> str:
    """
    Convierte un timestamp en una cadena con formato "YYYY-MM-DD HH:MM:SS".

    Args:
        timestamp (float): El timestamp a formatear.

    Returns:
        str: La cadena formateada.
    """
    datetime_obj = datetime.fromtimestamp(timestamp)
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime


# %%
class scraper:  
    def search_people(config: Dict[str, str]) -> DataFrame:
      global user_id
      init_cli()
      
      is_search:bool = config["is_search"]
      profiles_to_search:List[str] = config["profiles_to_search"]
      urls_profiles = []
      df:DataFrame = pd.DataFrame()
      driver = None
      # Crear una instancia
      print(CHROME_DRIVER_PATH)
      try:
        driver = webdriver.Chrome("C:\\Users\\urieh\\Documents\\FORTE\\META\\chromedriver-win64\\chromedriver.exe")
      except Exception as e:
        print(e)
        print("Error al crear el driver")
        error =insert_error({
          "timestamp": format_timestamp(time.time()),
          "state": "unlogged",
          "error_message": "Error al crear el driver",
          "request_url": "No aplica",
          "stack_trace": "No aplica",
          "additional_info": "No se pudo crear el driver",
          "user_id": user_id
        })
        print(error)
        return
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
      time.sleep(2)
      if is_logged(driver) is True:
        insert_error({
          "timestamp": format_timestamp(time.time()),
          "state": "unlogged",
          "error_message": "No se pudo iniciar sesion, ingrese primero a linkedin",
          "request_url": "No aplica",
          "stack_trace": "No aplica",
          "additional_info": "No se pudo iniciar sesion",
          "user_id": user_id
        })
        return
      if is_search:
        df = search_by_urls(driver,profiles_to_search)
      else:
        df = search_by_keyword(driver,config,urls_profiles)
      driver.quit()
      return df
    


# %%
import requests
import json
def insert_config(config:Dict[str, Any]) -> Dict[str, Any]:
    #convertir is_search de boolean a numero
  config["is_search"] = 0 if config["is_search"] is False else 1
  #convertir profiles_to_search a string
  config["profile_url"] = ",".join(config["profiles_to_search"])
  headers = {
    'Content-Type': 'application/json'
  }
  json_data = json.dumps(config)
  request = requests.post("http://127.0.0.1:8787/search", headers=headers, data=json_data)
  return request.json()

# %%
user_id = -1

# %%
from model.config import ConfigScrap

# def lambda_handler(event, context):
#     global user_id
#     config = ConfigScrap(**event).__dict__
#     id =insert_config(config)
#     user_id = id["oki"]["lastId_search"]
#     df =  scraper.search_people(config)

#     if df is not None:
#         df.to_csv(CSV_FILE_PATH, index=False)
#         return 'Scraping finalizado'
#     else:
#         return 'Error al hacer scraping'
# event ={
#     "keyword": "java developer",
#     "location": "leon",
#     "initial_page": 1,
#     "final_page": 4,
# }

# lambda_handler(event, None)


# %%


# %%
import pandas as pd


def get_data():
    return pd.read_csv('profiles.csv')


# def main():
#     data = get_data()
#     #saber el total de filas
#     total_rows = data.shape[0]
#     print(f"Total de filas: {total_rows}")

# if __name__ == '__main__':
#     main()

# %%
#run scraper
from model.config import ConfigScrap
basic_config = {
    "keyword": "vue",
    "location": "Leon, Guanajuato",
    "initial_page": 1,
}

# medium_config = {
#     "keyword": "vue",
#     "location": "leon",
#     "initial_page": 1,
#     "final_page": 4,
# }

# search_config = {
#   "keyword": "diseñador",
#     "profiles_to_search": ["https://mx.linkedin.com/in/nanadiseno","https://mx.linkedin.com/in/luisfernando-celaya"],
#     "is_search": True,
# }

