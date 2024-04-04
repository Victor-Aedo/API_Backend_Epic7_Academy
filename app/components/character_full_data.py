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




async def fetch_characters(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f'Error en la solicitud: {response.status_code}')


async def character_data():
    url = 'https://epic7x.com/stats-filter/'
    html = await fetch_characters(url)
    
    start_index = html.find('var CHARACTERS = ')
    end_index = html.find('var TAGS =')
    script_content = html[start_index + 16:end_index]

    script_content = re.sub(r';\s*$', '', script_content)

    characters_json = json.loads(script_content)

    print(characters_json)