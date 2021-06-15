from flask import render_template
from ..app import *

import xml.etree.ElementTree as ET
import json


@app.route("/")
def home():
    return render_template("pages/home.html")



def getJSON(path):
    """
    Get data from a JSON file 
    :param path: str
    :return: data
    :rtype: dict
    """
    with open(path, encoding="iso-8859-15" ) as data_file:
       data = json.load(data_file)
    return data;

def make_cmif(file:str):
    tree = ET.parse(file)
    root = tree.getroot()

    toremove= []

    for child in root[0][1]:
        if "corresp" not in child.attrib:
            toremove.append(child)

    for child in toremove:
        root[0][1].remove(child)
    
    tree.write('data/output.xml',
           xml_declaration=True, encoding='utf-8',
           method="xml")
        


