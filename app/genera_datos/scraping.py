# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 08:05:00 2018

@author: Usuario
"""

from selenium import webdriver
from time import time
import genera_Y_R as g

driver = webdriver.Chrome()

continua = True
pagina = 1
pag = 0
n_juegos = 0
tiempo = time()
csvfile = open('../static/datos/datosJuegos.csv', 'w')

while continua:

    webSite = "https://archive.org/details/softwarelibrary_c64_games?&sort=-downloads&page=" + str(pagina)
    try:
        driver.get(webSite)

        # En elem: Nombre_Juego, Empresa, eye, favorite, comment
        elem = driver.find_elements_by_xpath("//div [@class='item-ia hov']")

        # En elem2 Imagenes Links
        elem2 = driver.find_elements_by_class_name("item-img ")

        if len(elem) > 0:
            n_juegos = n_juegos +  len(elem)
            pag = pag+1
            pagina = pagina +1

            i=0
            while i < len(elem):
                juego = elem[i].text.split('\n')
                long= len(juego)
                juego[1] = juego[1][3:]

                link = elem2[i].get_attribute('src').split('/')
                link_ok = link[len(link)-1]

                #Corrige coma en separación miles
                vistas = juego[long-5]
                pos_coma = vistas.find(",")
                if pos_coma >= 0:
                    n = int(vistas[: pos_coma])*1000
                    for j in range(len(vistas)-pos_coma-1):
                        n = n + (int(vistas[j+pos_coma+1]) * 10**(2-j))
                    vistas = str(n)
				# fin Corrige coma

                csvfile.write(juego[0]+";"+juego[1]+";"+vistas+";"+juego[long-3]+";"+juego[long-1]+";"+link_ok+"\n")
                i = i+1
        else:
            continua = False

        print("   --> Paginas Analizadas   : ", pag)
        print("   --> Juegos Referenciados : ", n_juegos)

    except:
        continua = False



csvfile.close()
driver.close()


# Genera tablas Y, R, P_Modelos, P_Men_Users y P_Mem_Juegos
#   Evitamos utilziar en futuro datos desfasados para filtros
g.genera_tablas(n_juegos)


print("\n-------  Resultados del Scraping --------")
print("   --> Paginas Analizadas   : ", pag)
print("   --> Juegos Referenciados : ", n_juegos)
print("   --> Tiempo               : %.2f segundos" %(time()-tiempo))

# 17.000  = 134 páginas
# /services/img/Castle_Wolfenstein_1983_Muse_Software
#/details/Castle_Wolfenstein_1983_Muse_Software
# Opción todas juntas
#elem = driver.find_element_by_id("ikind--downloads")