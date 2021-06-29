from werkzeug.utils import secure_filename
from flask import flash
import xml.etree.ElementTree as ET
import json

from ..app import *


def add_selected_matchs(selected: dict):
    """
    Add the kalliope link for selected matchs by user
    and store the updated letters in matchs.xml
    :param selected: dict
    """
    tree = ET.parse('app/data/matchs.xml')
    root = tree.getroot()

    for match in selected:
        # Data from the template's form
        link = match.split(", '")[5].split("', ")[0]
        sender = match.split(", '")[1].split("']")[0]
        addressee = match.split(", '")[1].split("']")[1].split("['")[1].split("'")[0]
        date = match.split(", '")[3].split("']")[0]
        place = match.split(", '")[4].split("']")[0]

        for child in root[0][1]:
            try :
                cs_sender = child[0][0].attrib["ref"]
                cs_addressee = child[1][0].attrib["ref"]
                cs_place = child[0][1].text
                cs_date = child[0][2].attrib["when"]
            except: pass

            if cs_sender == sender and cs_addressee == addressee and cs_date == date and cs_place == place:
                child.set('corresp', link)
    
    tree.write('app/data/matchs.xml',
           xml_declaration=True,encoding='utf-8',
           method="xml")


def count_corresp(file:str):
    """
    Return the count of letters with the attribute @corresp.
    :param file: str
    :return: count
    :rtype: int
    """
    tree = ET.parse(file)
    root = tree.getroot()
    count = 0

    for child in root[0][1]:
        if "corresp" in child.attrib:
            count +=1
        
    return count

def make_cmif(file:str):
    """
    Create the CMIF file of matching letters.
    :param file : str
    """
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


def upload_file(file):
    """
    Upload a file inputed by user
    :param file : str
    """
    try:
        file.save(os.path.join(data, secure_filename(file.filename)))
    except Exception as E:
        print(E)
        flash(
            "Error during the upload of the file.",
            category="error",
        )
