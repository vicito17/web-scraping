"""
OBJETIVO:
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ABRIL 2020
"""
import random
from time import sleep
from selenium import webdriver # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
direccion_driver="/home/vicentecipre/.wdm/drivers/chromedriver/linux64/78.0.3904.105/chromedriver"
driver = webdriver.Chrome(direccion_driver) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

# Voy a la pagina que requiero
driver.get('https://www.olx.com.ec ')
driver.refresh() # Solucion de un bug extraño en donde los anuncios solo cargan al hacerle refresh o al darle click a algun elemento

sleep(5) # Esperamos que cargue el boton
# Busco el boton para cargar mas informacion
for i in range(3): # Voy a darle click en cargar mas 3 veces
    try:
        boton= WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH,'//button[@data-aut-id="btnLoadMore"]')
            ))
         # le doy click
        boton.click()
        # espero que cargue la informacion dinamica
        sleep(random.uniform(8.0, 10.0))
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH,'//li[@data-aut-id="itemBox"]//span[]data-out-id="itemPrice"')
            ))
    except:
        # si hay algun error, rompo el lazo. No me complico.
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')


# Recorro cada uno de los anuncios que he encontrado
for anuncio in anuncios:
    # Por cada anuncio hallo el precio
    precio = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    print (precio)
    # Por cada anuncio hallo la descripcion
    descripcion = anuncio.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    print (descripcion)