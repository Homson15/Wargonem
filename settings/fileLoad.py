import json
import os

import Logs.logs as log

def getColors():

    try:
        f = open(os.path.join("assets", "color_palette.json"))
        colors = json.load(f)
        f.close()

        return colors
    except FileNotFoundError:
        log.println("Error: Cannon find color_palette.json file")
        return "404"


def getItems():

    try:

        f = open(os.path.join("assets", "items.json"))
        items = json.load(f)
        f.close()

        return items
    except FileNotFoundError:
        log.println("Error: Cannot find item list")
        return "404"

def getTiles():

    try:

        f = open(os.path.join("assets", "tiles.json"))
        tiles = json.load(f)
        f.close()

        return tiles

    except FileNotFoundError:
        log.println("Error: Cannot find tile info")
        return "404"


def getMap(file):

    try:

        f=open(os.path.join("assets", "map", file))
        tab = []
        for line in f:
            tab.append(line.replace("\n",""))
        f.close()


        return tab
    except FileNotFoundError:
        log.println(f"Error: Cannot find {file}")
        return "404"