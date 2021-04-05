# -*- coding: utf-8 -*-
"""
OBJETIVO:
    - Extraer el precio, titulo y descripcion de productos en Mercado Libre.
    - Aprender a realizar extracciones verticales y horizontales con Selenium.
    - Demostrar que Selenium no es optimo para realizar extracciones que requieren traversar mucho a traves de varias pagina de una web
    - Aprender a manejar el "retroceso" del navegador
    - Aprender a definir user_agents en Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ABRIL 2020
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options

# Definimos el User Agent en Selenium utilizando la clase Options
direccion_driver="/home/vicentecipre/.wdm/drivers/chromedriver/linux64/78.0.3904.105/chromedriver"
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome(direccion_driver, chrome_options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

#URL SEMILLA
driver.get('https://www.idealista.com/alquiler-oficinas/madrid-madrid/')


# LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
PAGINACION_MAX = 10
PAGINACION_ACTUAL = 1

# Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
caja= r'(//article[@class="item item_contains_branding item-multimedia-container"])['
while True:

    for i in range(len(driver.find_elements(By.XPATH, '//article[@class="item item_contains_branding item-multimedia-container"]'))):
        print(i)
        direc_bas= caja + str(i) + ']'
        print(direc_bas)
        link = driver.find_element(By.XPATH, direc_bas + r'/div/a')#.get_attribute("href")
        direccion= driver.find_element(By.XPATH, direc_bas + r'/div/a/text()')
        precio= driver.find_element(By.XPATH, direc_bas + r'/div/div').text()
        m_2= driver.find_element(By.XPATH, direc_bas + r'/div/span').text()
        print(link,direccion,precio,m_2)
        print("#"*100)
    # print(links_productos)
    # links_de_la_pagina = []
    # for a_link in links_productos:
    #     print(a_link.find_elements(By.XPATH,'//div[@class="row price-row clearfix"]'))
    #     sleep(5)
    #     print("#"*100)
        # print(a_link)
        # print("#"*100)
        # titulo = driver.find_element(By.XPATH, '//h1').text
        # precio = driver.find_element(By.XPATH, '//span[@class="price-tag-fraction"]').text
        # print (titulo)
        # print (precio.replace('\n', '').replace('\t', ''))
#
    # # Logica de deteccion de fin de paginacion
    # try:
    #     # Intento obtener el boton de SIGUIENTE y le intento dar click
    #     puedo_seguir_horizontal = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
    #     puedo_seguir_horizontal.click()
    # except:
    #     # Si obtengo un error al intentar darle click al boton, quiere decir que no existe
    #     # Lo cual me indica que ya no puedo seguir paginando, por ende rompo el While
    #     break
    #
    # PAGINACION_ACTUAL += 1