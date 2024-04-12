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
from PIL import Image
import httpx
from app.components.links_artifacts import artifact_links

async def fetch_artifacts(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f'Error en la solicitud: {response.status_code}')

async def get_artifacts():

    url = 'https://epic7x.com/artifacts/'
    html = await fetch_artifacts(url)
    
    start_index = html.find('var ARTIFACTS = ')
    end_index = html.find('console.log (ARTIFACTS);')
    script_content = html[start_index + 16:end_index]

    script_content = re.sub(r';\s*$', '', script_content)

    artefacts = json.loads(script_content)

    artefacts_formatted = [
        {
            'name': object['name'],
            'class': object['class'],
            'rarity': object['rarity'],
            'image': object['image']
        }
        for object in artefacts
    ]

    artefactos_faltantes = [
        {'name': 'lela Violin', 'class': 'Mage', 'rarity': '4', 'image': ''},
        {'name': 'VII The Chariot', 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': 'VI The Lovers', 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': 'VI The Star', 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': 'Record of Unity', 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': "New Year's of Festival Souvenir", 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': 'Cutie Pando', 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': 'Our Beautiful Seasons', 'class': 'Any Class', 'rarity': '4', 'image': ''},
        {'name': 'One Year of Gratitude', 'class': 'Any Class', 'rarity': '4', 'image': ''}
    ]
    artefacts_formatted.extend(artefactos_faltantes)

    class HTMLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.fed = []

        def handle_data(self, d):
            self.fed.append(d)

        def get_data(self):
            return ''.join(self.fed)

    def decode_html_entities(text):
        stripper = HTMLStripper()
        stripper.feed(text)
        return stripper.get_data()

    for artefact in artefacts_formatted:
        if '&' in artefact['name']:
            artefact['name'] = decode_html_entities(artefact['name'])
        # custom_print(artefact['name'])  
        


    def add_image_links(artefacts_links):

        for artefact in artefacts_formatted:
            for url in artifact_links:
                
                # dejar solo el nombre
                nombre_archivo = url.split("/")[-1]
                
                # Eliminar la extensión del archivo ".webp"
                nombre_sin_extension = nombre_archivo.split(".")[0]

                

                if artefact['name'].count("-") > 0  and artefact['name'] == nombre_sin_extension:
                    artefact['image'] = url
                    

                else:
                    nombre_sin_guiones = nombre_sin_extension.replace("-", " ")
                    
                    if artefact['name'] == nombre_sin_guiones:
                        artefact['image'] = url
                        

                    
        


    add_image_links(artifact_links)



    return artefacts_formatted

    # # Ruta al directorio que contiene las imágenes
    # directory_path = './static/images/Artifacts'
    # absolute_path = os.path.abspath(directory_path)

    # # Función para leer y convertir una imagen a base85
    # def image_to_base85(file_path):
    #     with open(file_path, 'rb') as f:
    #         image_data = f.read()
    #         base85_data = base64.b85encode(image_data).decode('utf-8')
    #     return base85_data

    # # Función para obtener y convertir todas las imágenes en base85 y almacenarlas en un array de objetos
    # def convert_images_to_base85(directory_path):
    #     base85_images = []
    #     for filename in os.listdir(directory_path):
    #         if filename.endswith(('.webp')):  # Filtrar solo archivos de imagen
    #             for object in artefacts_formatted:
                    
    #                 if object['name'] == os.path.splitext(filename)[0]:
    #                     file_path = os.path.join(directory_path, filename)
    #                     base85_data = image_to_base85(file_path)
    #                     base85_images.append({'name': object['name'], 'class': object['class'], 'rarity': object['rarity'], 'image': base85_data})
        
    #     return base85_images

    # # Llamar a la función para obtener y convertir las imágenes
    # base85_images = convert_images_to_base85(directory_path)
    
    # # Imprimir los artefactos formateados

    # return base85_images