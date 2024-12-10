import pandas as pd


rute_csv = './static/e7HeroData.csv'

class Character:
    def __init__(self, name,rarity,classe,horoscope,element,attack,health,defense,crit_chance,crit_damage,effectiveness,effectiveness_resistance,speed,icon=0,model=0):
        self.name=name
        self.rarity=rarity
        self.classe=classe
        self.horoscope=horoscope
        self.element=element
        self.attack=attack
        self.health=health
        self.defense=defense
        self.crit_chance=crit_chance
        self.crit_damage=crit_damage
        self.effectiveness=effectiveness
        self.effectiveness_resistance=effectiveness_resistance
        self.speed=speed
        self.icon=icon
        self.model=model
        
    def __str__(self):
        return f"Name: {self.name}, Rarity: {self.rarity}, Class: {self.classe}, Horoscope: {self.horoscope}, Element: {self.element}, Attack: {self.attack}, Health: {self.health}, Defense: {self.defense}, Crit Chance: {self.crit_chance}, Crit Damage: {self.crit_damage}, Effectiveness: {self.effectiveness}, Effectiveness Resistance: {self.effectiveness_resistance}, Speed: {self.speed}"

def leer_csv():

    df = pd.read_csv(rute_csv)
    # print(df.head())
    # Inicializar una lista para almacenar objetos Persona
    characters = []

    # Iterar sobre cada fila del DataFrame
    for indice, fila in df.iterrows():
        # Crear un objeto Persona para esta fila y agregarlo a la lista
        character = Character(name=fila['name'], rarity=fila['rarity'], classe=fila['class'],horoscope=fila['horoscope'],element=fila['type'],attack=fila['attack'],health=fila['health'],defense=fila['defense'], crit_chance=fila['crit chance'],crit_damage=fila['crit damage'],effectiveness=fila['effectiveness'],effectiveness_resistance=fila['effectiveness resistance'],speed=fila['speed'])
        characters.append(character)
        # print(character)

    return characters