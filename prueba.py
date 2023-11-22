from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from bs4 import BeautifulSoup
import os
import time
import csv
from typing import Dict, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

load_dotenv()

def get_one_profile(driver,curren_url: str):
    # obtener el codigo de la pagina
    src = driver.page_source
    soup = BeautifulSoup(src)
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

def scrap_data_from_profile(driver,urls_profiles: List[str]):
  data_profiles = []
  for url in urls_profiles:
      driver.get(url)
      try:
         time.sleep(5)
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


def search_by_keyword(driver,config: Dict[str, str],urls_profiles: List[str]):
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
      print(f"site:linkedin.com/in/ AND {keywords} AND {location}")
      input_search.submit()

      for _ in range(final_page):
        time.sleep(5)

              # Obtener el código fuente de la página de resultados de búsqueda
        src = driver.page_source

              #pasear el html
        soup = BeautifulSoup(src)
        print(soup)

        profiles = soup.find_all('div', class_='MjjYud')

        for profile in profiles:
          profile_linkedin_url = profile.find('a')['href']
          try:
            if profile_linkedin_url.startswith('/search'):
              break
            urls_profiles.append(profile_linkedin_url)
          except Exception as e:
            print(e)
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
      
      return info
      
def is_logged(driver):
    #ver si hay un elemento con la clase form__input--text input_verification_pin
    try:
        driver.find_element(By.CLASS_NAME, 'form__input--text input_verification_pin')
        return True
    except Exception:
        return False
    
def insert_error(error):
    pass
def search_by_urls(driver,urls_profiles: List[str]):
    info = []
    try:
      info = scrap_data_from_profile(driver, urls_profiles)
      print(info)
    except Exception as e:
      print(e)
      print("Error al obtener los datos")
      return None
    return info

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
    
class scraper:  
    def search_people(config: Dict[str, str]):
      is_search:bool = config["is_search"]
      print({
         "is_search": is_search,
      })
      profiles_to_search:List[str] = config["profiles_to_search"]
      urls_profiles = []
     
      driver = None
      try:
        options = Options()
        # options.binary_location = '/opt/headless-chromium'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("C:\\Users\\urieh\\Documents\\FORTE\\META\\chromedriver-win64\\chromedriver.exe", options=options)
      except Exception as e:
        print(e)
        print("Error al crear el driver")
        return
      # Logging into LinkedIn
      driver.get('https://linkedin.com/uas/login')
      time.sleep(2)
      
      user = os.environ['USERNAME_LINKEDIN']
      password = os.environ['PASSWORD_LINKEDIN']

      try:
        username = driver.find_element(By.ID, "username")
        username.send_keys(user)

        pword = driver.find_element(By.ID, "password")
        pword.send_keys(password)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
      except Exception as e:
        print(e)
        print("Error al iniciar sesion")
        return None
      time.sleep(2)
      if is_logged(driver) is True:
        print('inicia sesion primero')
        return None
      print(is_search)
      if is_search is False:
       df = search_by_keyword(driver,config,urls_profiles)
      else:
        df = search_by_urls(driver,profiles_to_search)
      driver.quit()
      return df

def lambda_handler(event, context):
    df = scraper.search_people(event)
    if df is not None:
        print('funciono')
        return {
            "ok":200
        }
    else:
        print('no hay datos')
        return {
            "ok":500
        }


event = {
    "keyword": "vue",
    "location": "Leon, Guanajuato",
    "initial_page": 1,
    "final_page": 1,
    "is_search": False,
    "profiles_to_search":['https://www.linkedin.com/in/malva-sofia-rosales-casta%C3%B1eda-59b7aa298/']
}

lambda_handler(event, None)
