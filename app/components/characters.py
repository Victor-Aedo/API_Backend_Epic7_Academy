from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
import os
import base64
from app.components.custom_print import custom_print
import requests
import json
import re
from urllib.request import urlopen, Request
import libsql_client 
import asyncio
import html
from html.parser import HTMLParser
from typing import List

import httpx
from app.components.characters_csv import leer_csv
from app.components.decodificador_html import decode_html_entities
from app.components.links_icons_heroes import icons_heroes
from app.components.links_models_heroes import models_heroes


characters = []
character_faltante = []
characters_csv = leer_csv()
# Directorio de entrada con imágenes PNG
directorio_entrada = './static/images/icons'
# Directorio de salida para las imágenes convertidas a WebP
directorio_salida = './static/images/icons'

directory_path_models = './static/images/Character_Model'
# #Ruta al directorio que contiene las imágenes
directory_path = './static/images/icons'
absolute_path = os.path.abspath(directory_path)

async def fetch_characters(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            return response.text
        
        else:
            raise Exception(f'Error en la solicitud: {response.status_code}')




async def character_list():

    url = 'https://epic7x.com/stats-filter/'
    html = await fetch_characters(url)
    
    start_index = html.find('var CHARACTERS = ')
    end_index = html.find('var TAGS =')
    script_content = html[start_index + 16:end_index]

    script_content = re.sub(r';\s*$', '', script_content)

    characters_json = json.loads(script_content)

    for objecto in characters_json:
        character = {
            'name': objecto['name'],
            'class': objecto['class'],
            'rarity': objecto['rarity'],
            'horoscope': '', #Inicializado
            'element': '', #Inicializado
            'icon': '', #Inicializado
            'model': '', #Inicializado
            'attack': objecto['stats']['attack'],
            'health': objecto['stats']['health'],
            'defense': objecto['stats']['defense'],
            'speed': objecto['stats']['speed'],
            'critical_hit_chance': objecto['stats']['critical_hit_chance'],
            'critical_hit_damage': objecto['stats']['critical_hit_damage'],
            'effectiveness': objecto['stats']['effectiveness'],
            'effect_resistance': objecto['stats']['effect_resistance'],
            'awakening': objecto['awakening'],
            'skills': []  # Inicializar la lista de habilidades para cada personaje
            
        }


        for habilidad in objecto['skills']:
            skill_data = {
                'name': habilidad['skill_name'],
                'skill_type': habilidad['skill_type'],
                'special_acquired': habilidad['special_acquired'],
                'special_used_acquired': habilidad['special_used_acquired'],
                'skill_burn_effect': habilidad['skill_burn_effect'],
                'souls_obtained': habilidad['soul_required'],
                'description': re.sub(r'<.*?>', '', habilidad['description']),  # formatear la descripcion, está en html
                'skill_enhancement': habilidad['skill_enhancement'],
                'image': habilidad['image']['url'],  # No está presente en el objeto de habilidad
                'cooldown': habilidad['cooldown']
            }
            character['skills'].append(skill_data)  # Agregar las habilidades al personaje
        
        characters.append(character)  # Agregar el personaje al arreglo de personajes



     
    decode_heroe_names()

    # for character in characters:
    # # Reemplaza el carácter especial en el nombre del héroe
    #     

    agregar_horoscope()

    Agregar_characters_faltantes()

    agregar_icons(icons_heroes)

    agregar_models(models_heroes)

    for terminado in characters:
        print(terminado)
    
    # print(icons)
    # convertir_png_a_webp(directorio_entrada, directorio_salida) # Llamar a la función para obtener y convertir las imágenes a webp
    
    # convert_images_to_base85(directory_path, 'icon') # Llamar a la función para obtener y convertir las imágenes a base85
    
    # convert_images_to_base85(directory_path_models, 'model')

    return characters
    # for objeto in characters:
    #     print('name: ',objeto['name'], 'class: ',objeto['class'], 'element: ', objeto['element'])
    
    # for objeto in characters:
    #     # print('name: ',objeto['name'], 'class: ',objeto['class'], 'element: ', objeto['element'])
    #     encontrado = False
    #     if (objeto['icon']):

    #         encontrado = True
    #     else:

    #         print('name: ',objeto['name'], 'icon: ',encontrado)
    

    





def agregar_horoscope():
    #Agregar el Horoscopo a los heroes tomados de la pagina epic7x usando la informacion del csv
    for objeto in characters:
        for character in characters_csv:
            if objeto['name'].lower() == character.name.lower():
                objeto['horoscope'] = character.horoscope
                objeto['element'] = character.element
        # print(objeto)    
    
def decode_heroe_names():
    # Decodifica el nombre de los heroes que tengan codificacion html
    for objeto in characters:
        if '&' in objeto['name']:
            objeto['name'] = decode_html_entities(objeto['name'])
            objeto['name'] = objeto['name'].replace('’', "'")
        # custom_print(objeto['name'])

def buscar_characters_faltantes():
     # Encuentra lo heroes que faltan usando el csv de referencia y los almacena en el array "character_faltante"
    for character in characters_csv:
        encontrado = False  # Reiniciar para cada personaje en characters_csv
        for objeto in characters:
            if (character.name.lower() == objeto['name'].lower()):
                encontrado = True
                
        
        if not encontrado:
            character_faltante.append(character.name.lower())  
            # print(character.name.lower())

    
def Agregar_characters_faltantes():
    #Crea un objeto con todas las propiedades del heroe y se llena con la informacion del csv, luego estos heroes se agregan al array original de heroes
    buscar_characters_faltantes()

    character_faltantes = {}
    for faltantes in character_faltante:
            for character_csv in characters_csv:
                if (faltantes.lower() == character_csv.name.lower()):
                    # print(character_csv)
                    character_faltantes={
                        'name': character_csv.name,
                        'class': character_csv.classe,
                        'rarity': character_csv.rarity,
                        'horoscope': character_csv.horoscope,
                        'element': character_csv.element,
                        'icon': '', #inicializado
                        'model': '', #inicializado
                        'attack': character_csv.attack,
                        'health': character_csv.health,
                        'defense': character_csv.defense,
                        'speed': character_csv.speed,
                        'critical_hit_chance': character_csv.crit_chance,
                        'critical_hit_damage': character_csv.crit_damage,
                        'effectiveness': character_csv.effectiveness,
                        'effect_resistance': character_csv.effectiveness_resistance,
                        'awakening': '',
                        'skills': []  #inicializado
                        
                    }
                    characters.append(character_faltantes)
    
    



def agregar_icons(icons):
    for heroes in characters:
        for url in icons:
            # dejar solo el nombre
            nombre_archivo = url.split("/")[-1]
            # Eliminar la extensión del archivo ".webp"
            nombre_sin_extension = nombre_archivo.split(".")[0]

            if heroes['name'].count("-") > 0  and heroes['name'] == nombre_sin_extension:
                heroes['icon'] = url

            else:
                nombre_sin_guiones = nombre_sin_extension.replace("-", " ")
                if heroes['name'] == nombre_sin_guiones:
                    heroes['icon'] = url


                
def agregar_models(models):
    for heroes in characters:
        for url in models:
            
            # dejar solo el nombre
            nombre_archivo = url.split("/")[-1]
            # Eliminar la extensión del archivo ".webp"
            nombre_sin_extension = nombre_archivo.split(".")[0]

            if heroes['name'].count("-") > 0  and heroes['name'] == nombre_sin_extension:
                heroes['model'] = url

            else:
                nombre_sin_guiones = nombre_sin_extension.replace("-", " ")
                if heroes['name'] == nombre_sin_guiones:
                    heroes['model'] = url

























# Función para leer y convertir una imagen a base85
# def image_to_base85(file_path):
#     with open(file_path, 'rb') as f:
#         image_data = f.read()
#         base85_data = base64.b85encode(image_data).decode('utf-8')
#     return base85_data

# # Función para obtener y convertir todas las imágenes en base85 y almacenarlas en un array de objetos
# def convert_images_to_base85(directory_path, property):
#     for filename in os.listdir(directory_path):
#         if filename.endswith(('.webp')):  # Filtrar solo archivos de imagen
#             for  objeto in characters:
#                 if (objeto['name'] == os.path.splitext(filename)[0]):
#                     file_path = os.path.join(directory_path, filename)
#                     base85_data = image_to_base85(file_path)
#                     objeto[property] = base85_data

        
                    































                              
def convertir_png_a_webp(directorio_entrada, directorio_salida):
    # Comprueba si el directorio de salida existe, si no, créalo
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    # Itera sobre todos los archivos en el directorio de entrada
    for filename in os.listdir(directorio_entrada):
        if filename.endswith('.png'):
            # Abre la imagen PNG
            ruta_entrada = os.path.join(directorio_entrada, filename)
            imagen = Image.open(ruta_entrada)

            # Obtiene el nombre del archivo sin la extensión
            nombre_archivo = os.path.splitext(filename)[0]

            # Define la ruta de salida con la extensión .webp
            ruta_salida = os.path.join(directorio_salida, f"{nombre_archivo}.webp")

            # Guarda la imagen en formato WebP
            imagen.save(ruta_salida, 'WEBP')

            print(f"Imagen convertida: {ruta_salida}")



    


    



    