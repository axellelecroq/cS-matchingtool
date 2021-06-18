from flask import render_template, flash, request
from werkzeug.utils import secure_filename
from ..app import *


import xml.etree.ElementTree as ET
import json


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method.lower() == "post":
        if request.files["records"]:
            records = request.files["records"]
            records.filename = "records.json"
            upload_image(records)

            flash(
                "All good.",
                category="success",
            )

    return render_template("pages/home.html")


def upload_image(file):
        try:
            file.save(os.path.join(data, secure_filename(file.filename)))
        except Exception as E:
            print(E)
            flash(
                "Error during the upload of the file.",
                category="error",
            )

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
        


