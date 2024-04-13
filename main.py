from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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
from dotenv import load_dotenv
from app.components.artifacts import get_artifacts
from app.components.characters_csv import leer_csv
from app.components.characters import character_list
from app.components.test_blob import character_list_image





#Iniciar entorno virtual "ev\Scripts\activate"
#Iniciar el Server "uvicorn main:app --reload"
load_dotenv()
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

heroe=None
heroes = []

@app.get("/")
async def root():
    # global heroes
    # await insert_artifacts()
    # await deleteData()
    # await insert_test(artefacts)
    # await select_character()
    # leer_csv()
    await characters()
    # await test_image()
    # await select_character()
    
    return 'heroes'

@app.get("/hola")
async def root():
    global heroes
    
    return heroes
 

artefacts = []
@app.get("/artifacts")
async def root():
    global artefacts
    await select_artifacts()
    return artefacts

# Trae todos los heroes
@app.get("/Heros")
async def root():
    global heroes
    await select_heroes()
    return heroes

# Un solo heroe
@app.get("/Heros/{name}")
async def root(name: str):
    global heroe
    await select_heroe(name)
    return heroe




async def select_artifacts():
    global artefacts
    artefacts.clear()
    conn = await dbConnect()
    result = await conn.execute(f"SELECT * from artifact")

    # Obtener todas las filas como una lista de diccionarios
    rows = result.rows
    serialized_rows = [dict(row.asdict()) for row in rows]

    # Agregar las filas serializadas a la lista artefacts
    artefacts.extend(serialized_rows)



async def select_heroes():
    global heroes
    heroes.clear()
    conn = await dbConnect()
    result = await conn.execute(f"SELECT id_heroe, name, class, rarity, horoscope, element, icon from heroes")

    # Obtener todas las filas como una lista de diccionarios
    rows = result.rows
    serialized_rows = [dict(row.asdict()) for row in rows]

    # Agregar las filas serializadas a la lista artefacts
    heroes.extend(serialized_rows)


async def select_heroe(name):
    global heroe
    heroe.clear()
    conn = await dbConnect()
    result = await conn.execute(f"SELECT * FROM heroes WHERE name = '{name}'")
    rows = result.rows
    serialized_rows = [dict(row.asdict()) for row in rows]

    heroe = serialized_rows



async def insert_artifacts():
    artefacts = await get_artifacts()
    await insert_test(artefacts)























async def deleteData():
    conn = await dbConnect()
    result = await conn.execute("DELETE from artifact")


async def main():
    artefacts = await get_artifacts()
    # await select_test(table)

# async def select_test():
#     conn = await dbConnect()
#     result = await conn.execute("SELECT * from artifact")
#     custom_print(result.rows)



#Seteo de archivos estaticos
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


    

app.mount('/static', app=StaticFiles(directory=ruta), name="static")

url = os.getenv("URL")
authToken = os.getenv("AUTH_TOKEN")

async def dbConnect():
    return libsql_client.create_client(url = url, auth_token= authToken)


async def insert_test(artefacts):
    # result = await conn.execute("INSERT INTO artifact (name, artifact_class, rarity, image, hp, atk) VALUES ('Hola2', 'any', 4, 'hola', 0, 0)")
    for artefact in artefacts:
        conn = await dbConnect()
        print(artefact['name'])
        await conn.execute("INSERT INTO artifact (name, description, artifact_class, rarity, image, attack, health) VALUES (?, ? ,?, ?, ?, ?, ?)", (artefact['name'], 'description' , artefact['class'], artefact['rarity'], artefact['image'], 0, 0))
        await conn.close()    
    

async def select_character():
    
    conn = await dbConnect()
    result = await conn.execute("select * from heroes")
    custom_print(result.rows)

async def characters():
    result = await character_list()
    await insert_heroes(result)


async def insert_heroes(heroes):
    # result = await conn.execute("INSERT INTO artifact (name, artifact_class, rarity, image, hp, atk) VALUES ('Hola2', 'any', 4, 'hola', 0, 0)")
    
    for heroe in heroes:
        for skill in heroe['skills']:
            # conn = await dbConnect()
            
            heroe_name = heroe['name']
            name = skill['name']
            skill_type = skill['skill_type']
            special_acquired = skill['special_acquired']
            special_used_acquired = skill['special_used_acquired']
            skill_burn_effect = skill['skill_burn_effect']
            souls_obtained = skill['souls_obtained']
            description = skill['description']
            skill_enhancement = skill['skill_enhancement']
            image = skill['image']
            cooldown = skill['cooldown']
                
            print('heroes: ', heroe_name, 'skill: ', name, 'skill_type: ', skill_type, 'description: ', description)

            # await conn.execute("INSERT INTO skills (heroe_name, name, type, special_acquired, special_used_acquired, burn_effect, souls_obtained, description, enhancement, image, cooldown) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (heroe_name, name, skill_type, special_acquired, special_used_acquired, skill_burn_effect, souls_obtained, description, skill_enhancement, image, cooldown))
            # await conn.close()

                                                                                                                                                                                                                                             
                                                                                                

async def test_image():
    result = await character_list_image()
    await insert_test_image(result)



async def insert_test_image(result):
    # result = await conn.execute("INSERT INTO artifact (name, artifact_class, rarity, image, hp, atk) VALUES ('Hola2', 'any', 4, 'hola', 0, 0)")
    for test in result:
        conn = await dbConnect()
        name = test['name']
        image = test['image']
        print(test['name'], test['image'])
        await conn.execute("INSERT INTO test (name, image) VALUES (?, ?)", (test['name'], test['image']))
        await conn.close()


# characters=leer_csv()

# for character in characters:
#     # Imprimir los atributos de cada objeto
#     print("Name:", character.name)
#     print("Rarity:", character.rarity)
#     print("Class:", character.classe)
#     print("Horoscope:", character.horoscope)
#     print("Elemt:", character.element)
#     print("Attack:", character.attack)
#     print("Health:", character.health)
#     print("Defense:", character.defense)
#     print("Crit_Chance:", character.crit_chance)
#     print("Crit_Damage:", character.crit_damage)
#     print("Effectiveness:", character.effectiveness)
#     print("Effectiveness_Resistance:", character.effectiveness_resistance)
#     print("Speed:", character.speed)
#     print("Icon:", character.icon)
#     print("Model:", character.model)
#     print("-" * 20)  # Separador entre cada personaje


# async def heroes(characters):
#     # result = await conn.execute("INSERT INTO artifact (name, artifact_class, rarity, image, hp, atk) VALUES ('Hola2', 'any', 4, 'hola', 0, 0)")
 
        
#     for character in characters:

#         conn = await dbConnect()
#         print("Name:", character.name)
#         print("Rarity:", character.rarity)
#         print("Class:", character.classe)
#         print("Horoscope:", character.horoscope)
#         print("Attack:", character.attack)
#         print("Health:", character.health)
#         print("Defense:", character.defense)
#         print("Crit Chance:", character.crit_chance)
#         print("Crit Damage:", character.crit_damage)
#         print("Effectiveness:", character.effectiveness)
#         print("Effectiveness Resistance:", character.effectiveness_resistance)
#         print("Speed:", character.speed)
#         print("-" * 20)  # Separador entre cada personaje
#         await conn.execute("INSERT INTO artifact (name, artifact_class, rarity, image, hp, atk) VALUES (?, ?, ?, ?, 0, 0)", (name, artifact_class, rarity, image))
#         await conn.close()   














    








#   # Imprimir los artefactos formateados
#     for objeto in base85_images:
#         # Iterar sobre cada propiedad del objeto
#         for propiedad, valor in objeto.items():
#             # Imprimir la propiedad y su valor
#             custom_print(f'{propiedad}: {valor} \n')
#         # Imprimir un separador entre cada objeto
#         print('-' * 10)


















# # Ruta al directorio que contiene las imágenes PNG en el proyecto backend
# directory_path = './static/images/Artefactos_5_estrellas'
# absolute_path = os.path.abspath(directory_path)
# custom_print("Ruta absoluta del directorio:", absolute_path)

# # Función para convertir una imagen PNG a WebP
# def convert_to_webp(png_file):
#     # Abrir la imagen PNG
#     with Image.open(png_file) as img:
#         # Cambiar el formato a WebP y guardar la imagen con el mismo nombre pero extensión .webp
#         webp_file = os.path.splitext(png_file)[0] + ".webp"
#         img.save(webp_file, "WEBP")

#     return webp_file

# # Endpoint para transformar imágenes PNG a WebP
# @app.post("/convert_to_webp")
# async def convert_images_to_webp():
#     webp_files = []
#     # Recorrer todos los archivos en el directorio especificado
#     for filename in os.listdir(absolute_path):
#         # Verificar si el archivo es una imagen PNG
#         if filename.endswith(".png"):
#             # Obtener la ruta completa del archivo PNG
#             png_file_path = os.path.join(absolute_path, filename)
#             custom_print(png_file_path)
#             # Convertir el archivo PNG a WebP
#             webp_file = convert_to_webp(png_file_path)
#             webp_files.append(webp_file)
#     return {"webp_files": webp_files}







# url = 'https://epic7x.com/artifacts/'

# # Realizar la solicitud utilizando urllib
# request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# response = urlopen(request)

# # Verificar si la solicitud fue exitosa (código de respuesta 200)
# if response.getcode() == 200:
#     # Leer el contenido de la respuesta
#     html = response.read().decode('utf-8')
#     # print(html_read)
# else:
#     raise Exception('Error en la solicitud:', response.getcode())

# # Buscar el script que contiene la información necesaria
# start_index = html.find('var ARTIFACTS = ')
# end_index = html.find('console.log (ARTIFACTS);')
# script_content = html[start_index + 16:end_index]

# # Eliminar el punto y coma al final si existe
# script_content = re.sub(r';\s*$', '', script_content)

# # Convertir el contenido del script a un objeto Python
# artefacts = json.loads(script_content)

# # custom_print(artefacts)

# # Formatear los artefactos
# artefacts_formatted = [
#     {
#         'name': object['name'],
#         'class': object['class'],
#         'rarity': object['rarity'],
#         'image': object['image']
#     }
#     for object in artefacts
# ]


# artefactos_faltantes = [
#     {'name': 'lela Violin', 'class': 'Mage', 'rarity': '4', 'image': '1'},
#     {'name': 'VII. The Chariot', 'class': 'Any Class', 'rarity': '4', 'image': '1'},
#     {'name': 'VI. The Lovers', 'class': 'Any Class', 'rarity': '4', 'image': '1'},
#     {'name': 'VI. The Star', 'class': 'Any Class', 'rarity': '4', 'image': '1'},
#     {'name': 'Record of Unity', 'class': 'Any Class', 'rarity': '4', 'image': '1'},
#     {'name': "New Year's of Festival Souvenir", 'class': 'Any Class', 'rarity': '4', 'image': '1'},
#     {'name': 'Cutie Pando', 'class': 'Any Class', 'rarity': '4', 'image': ''},
#     {'name': 'Our Beautiful Seasons', 'class': 'Any Class', 'rarity': '4', 'image': '1'},
#     {'name': 'One Year of Gratitude', 'class': 'Any Class', 'rarity': '4', 'image': '1'}
# ]
# artefacts_formatted.extend(artefactos_faltantes)







# class HTMLStripper(HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.reset()
#         self.strict = False
#         self.convert_charrefs = True
#         self.fed = []

#     def handle_data(self, d):
#         self.fed.append(d)

#     def get_data(self):
#         return ''.join(self.fed)

# def decode_html_entities(text):
#     stripper = HTMLStripper()
#     stripper.feed(text)
#     return stripper.get_data()


# for artefact in artefacts_formatted:
#     if '&' in artefact['name']:
#         artefact['name'] = decode_html_entities(artefact['name'])
#         # custom_print(artefact['name'])
     

# for objecto in artefacts_formatted:
#     print(objecto['name'])

























# async def insert_artifacts(values):
    
#     conn = await dbConnect()
#     result = await conn.execute("""INSERT INTO nombre_tabla (name, class, rarity, image, hp, atk)
#     VALUES (?, ?, ?, ?, ?, ?)
#     """)
#     custom_print(result.rows)


# for objeto in base85_images:

#     # # Extraer los valores del objeto
#     valores = (objeto['name'], objeto['class'], objeto['rarity'], objeto['image'], 0, 0)
    

#     # Ejecutar la consulta de inserción
#     asyncio.run(insert_artifacts(valores))




# async def insert_artifacts(name, clase, rarity, image, hp, atk):
#     conn = await dbConnect()
#     result = await conn.execute(f"INSERT INTO artifact (name, class, rarity, image, hp, atk) VALUES ('{name}', '{clase}', '{rarity}', '{image}', '{hp}', '{atk}')")
   
#     return result  # Retorna el resultado de la consulta

# async def main():
#     for objeto in base85_images:
#         # Extraer los valores del objeto
#         name, clase, rarity, image, hp, atk = (objeto['name'], objeto['class'], objeto['rarity'], objeto['image'], 0, 0)
#         # Ejecutar la consulta de inserción
#         custom_print(name, clase, rarity, image, hp, atk)
#         result = await insert_artifacts(name, clase, rarity, image, hp, atk)
#         custom_print(result.rows)





















# Imprimir los artefactos formateados
# for objeto in base85_images:
#     # Iterar sobre cada propiedad del objeto
#     for propiedad, valor in objeto.items():
#         # Imprimir la propiedad y su valor
#         custom_print(f'{propiedad}: {valor} \n')
#     # Imprimir un separador entre cada objeto
#     print('-' * 10)






# # Función de autenticación
# def authenticate(token: str = None):
#     # Aquí debes implementar la lógica para verificar si el token es válido
#     # Por ejemplo, podrías comparar el token con uno almacenado en tu backend
#     if token == "TOKEN_VALIDO":
#         return True
#     else:
#         return False

# # Endpoint protegido para transformar imágenes PNG a WebP
# @app.post("/convert_to_webp")
# async def convert_images_to_webp(png_files: List[str], authenticated: bool = Depends(authenticate)):
#     # Verificar si el usuario está autenticado
#     if not authenticated:
#         raise HTTPException(status_code=401, detail="No autorizado")
    
#     # Aquí iría tu lógica para convertir las imágenes PNG a WebP
#     # Simplemente devolvemos un mensaje de éxito por ahora
#     return {"message": "Imágenes convertidas a WebP"}


















# # Imprimir los nombres de archivo y sus representaciones base64
# for image_obj in base64_images:
#     print(f"Imagen base64: {image_obj['image'][:50]}...")  # Imprimir solo los primeros 50 caracteres de la imagen base64

# custom_print(base64_images.items())


# # Abre la imagen como un archivo binario y lee su contenido
# with open(image_path, "rb") as f:
#     # Lee los bytes de la imagen
#     image_bytes = f.read()