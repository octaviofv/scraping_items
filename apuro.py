# librerias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os


# ruta driver
path_driver = "./chromedriver.exe"

# opciones de driver
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})

# definir driver
print("abriendo navegador")
driver = webdriver.Chrome(chrome_options=option, executable_path=path_driver)
driver.set_window_size(1600, 1024)

# definir web
driver.get("https://www.facebook.com/")

# rellenar usuario
print("iniciando sesion")
user_fb = input('indicar usuario: ')
input_usuario = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
input_usuario.clear()
input_usuario.send_keys(user_fb)

# rellenar contraseña
pw_fb = input('indicar contraseña: ') 
input_pw = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
input_pw.clear()
input_pw.send_keys(pw_fb)

# click iniciar sesion
print("dando click en boton iniciar sesion")
boton_inicio_sesion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='_6ltg']"))).click()

# ir al sitio de marketplace actualizando el enlace
busqueda = "apuro"
# por defecto 1 - 7 - 30 días
tiempo_busqueda_dias = 30
esperar_web = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='rq0escxv l9j0dhe7 du4w35lb j83agx80 g5gj957u pmt1y7k9 buofh1pr hpfvmrgz taijpn5t gs1a9yip owycx6da btwxx1t3 f7vcsfb0 fjf4s8hc b6rwyo50 oyrvap6t']")))
time.sleep(5)
print("realizando busqueda en marketplace")
driver.get("https://www.facebook.com/marketplace/santiagocl/search?daysSinceListed=" + str(tiempo_busqueda_dias) + "&query=" + busqueda + "&exact=false")

# hacer scroll down en el sitio
n_scrolls = 10
for i in range(1, n_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    esperar_productos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='l9j0dhe7 f9o22wc5 ad2k81qe']")))
    print("haciendo scroll down", i)

## obtener la data en tablas
# obtener estructura web para bs4
soup = BeautifulSoup(driver.page_source, 'html.parser')

cuadros = soup.findAll("div", attrs={"class":"rq0escxv j83agx80 cbu4d94t i1fnvgqd muag1w35 pybr56ya f10w8fjw k4urcfbm c7r68pdi suyy3zvx"})

precios = []
titulos = []

for cuadro in cuadros:
    precio = cuadro.find_all("span", attrs={"class":"d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id"})
    precio.replace(' ', '')
    precios.append(precio[0].text)
    titulo = cuadro.find_all("span", attrs={"class":"a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7"})
    titulos.append(titulo[0].text)

print(precios, titulos)

# pasar listas a df 
print('largo precios', len(precios))
print('')
print('largo titulos', len(titulos))

if len(precios) == len(titulos):
    print('guardando df')
    df = pd.DataFrame(list(zip(titulos, precios)), columns=['TITULOS', 'PRECIOS'])
    df.to_csv('./resultado_scraping.csv', encoding='UTF-8')
else:
    print('listas con distinto largo')


# cerrar driver
print("cerrando driver")
driver.quit()

