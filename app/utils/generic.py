from werkzeug.utils import secure_filename
from flask import flash
import xml.etree.ElementTree as ET
import json

from ..app import *


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


def upload_file(file):
        try:
            file.save(os.path.join(data, secure_filename(file.filename)))
        except Exception as E:
            print(E)
            flash(
                "Error during the upload of the file.",
                category="error",
            )


def make_cmif(file:str):
    tree = ET.parse(file)
    root = tree.getroot()

    toremove= []

    for child in root[0][1]:
        if "corresp" not in child.attrib:
            toremove.append(child)

    for child in toremove:
        root[0][1].remove(child)
    
    tree.write('app/data/output.xml',
           xml_declaration=True, encoding='utf-8',
           method="xml")


