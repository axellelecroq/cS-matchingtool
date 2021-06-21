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

    letter_toremove= []
    bibl_tokeep = []
    bibl_remove = []
    resp=[]
    resp_toremove=[]

    for child in root[0][1]:
        # If a kalliope link was stored in @corresp, it's mean that's a match.
        # If not, the letter should be remove of the CMIF file
        if "corresp" not in child.attrib:
            letter_toremove.append(child)
        else :
            # Source of matching letters is kept in a list. 
            if child.attrib['source'] not in bibl_tokeep:
                source_id = child.attrib['source'].split('#')[1]
                bibl_tokeep.append(source_id)
    
    # Clean the sourceDesc (bibliographie)
    for child in root[0][0][2]:
        if child.attrib['{http://www.w3.org/XML/1998/namespace}id'] not in bibl_tokeep:
            bibl_remove.append(child)
    for child in bibl_remove:
        root[0][0][2].remove(child)

    # Clean the respStmt (institutions)
    for child in root[0][0][0][1]:
        if child.text not in resp:
            resp.append(child.text)
        else :resp_toremove.append(child)
    for child in resp_toremove:
        root[0][0][0][1].remove(child)    

    # Clean the profileDesc (letters)
    for child in letter_toremove:
        root[0][1].remove(child)
    
    # Store the clean file
    tree.write('app/data/output.xml',
           xml_declaration=True, encoding='utf-8',
           method="xml")


