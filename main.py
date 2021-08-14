# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests


# ruta driver
path_driver = "./chromedriver.exe"

# definir driver
print("abriendo navegador")
driver = webdriver.Chrome(path_driver)

# definir web
driver.get("https://www.google.cl/")

# indicar busqueda
print("inicio busqueda")
busqueda = "perros"
barra_busqueda = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='q']")))
barra_busqueda.clear()
barra_busqueda.send_keys(busqueda)

# click buscar en google
print("click en boton  buscar")
boton_buscar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='btnK']"))).click()

# obtener la pagina de resultados
print("obtengo la informacion de la web")
soup = BeautifulSoup(driver.page_source, 'html.parser')

# listar enlaces
print("guardando enlaces")
lista_enlaces = []
enlaces = soup.findAll('h3', attrs={'class':'LC20lb DKV0Md'})
for enlace in enlaces:
    texto = enlace.text
    lista_enlaces.append(texto)

print(lista_enlaces)

# cerrar driver
print("cerrando driver")
driver.quit()

