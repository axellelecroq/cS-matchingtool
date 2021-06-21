
import xml.etree.ElementTree as ET
import json

from .generic import getJSON, make_cmif

def matching(file: str):
    tree = ET.parse('app/data/csdata.xml')
    root = tree.getroot()
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

    data = getJSON(file)

    for record in data:
        # Handling senders
        s_status = ""
    
        try :
            sender = ''
            for key in record.keys():
                if key == 'creator_gnd':
                    sender = record['creator_gnd']
            if sender == '' :
                if "," not in record["creator"] and "(" not in record["creator"] and type(record["creator"]) != list :
                    sender = record["creator"]
                elif type(record["creator"]) != list:
                    creator = record["creator"].split(" (")[0]
                    name = creator.split(", ")[0]
                    firstname = creator.split(", ")[1]
                    sender = firstname + " " + name
                else : 
                    sender = "Unbekannt" # 261 entrées avec une liste comme creator
                      # Gestion des listes d'envoyeur à faire
        except KeyError: 
            sender = "Unbekannt"
        except IndexError : 
            try :
                sender = record["creator"].split(" (")[0]
                if "," in record["creator"].split(" (")[1].split(", ")[1]:
                    s_status = record["creator"].split(" (")[1].split(", ")[1].split(", ")[0]
                else : s_status = record["creator"].split(" (")[1].split(", ")[1]
                if ")" in s_status :
                    s_status = s_status.replace(")", "")
            except IndexError : 
                sender = record["creator"].split("(")[0]
            
    # Handling addressee  
        try : 
            addressee =  '' 
            for key in record.keys():
                if key == 'subject_gnd':
                    addressee = record['subject_gnd']
        
            if addressee == '':
                addressee = record["subject"]
        except KeyError:
            addressee = "Unbekannt"
    
     # Handling date
        try :
            date = record["date"]

        except KeyError:
            date = "00-00-00"
        
    # Handling place
        try :
            place = record["coverage"]
            unbekannt = ["o. O.", "Ohne Ort", "o.O.", "o.D."]
            if place in unbekannt:
                place = ""
            if type(place) == list:
                place = "" # TODO gestion des listes dans place
        except : place = ""
    
    # ---- correspSearch
        for child in root[0][1]:
        # Handle sender
            try :
                cs_sender = child[0][0].attrib["ref"]
            except :
                cs_sender = child[0][0].text
                if cs_sender == None :
                    cs_sender = "Unbekannt"
        # Handle addresse        
            try:
                cs_addressee = child[1][0].attrib["ref"]
            except:
                cs_addressee = child[1][0].text
                if cs_addressee == None :
                    cs_addressee = "Unbekannt"
                
        # Handle place        
            try:
                cs_place = child[0][1].text
        
                if cs_place == None: 
                    try :
                        cs_place = child[0][2].text
                    except: 
                        cs_place = cs_place = child[1][1].text
            except: cs_place = "Unbekannt"
            
        # Handle date        
            try: 
                cs_date = child[0][2].attrib["when"]
            except:
                try : 
                    cs_date = child[0][1].attrib["when"]
                except: 
                    try : cs_date = child[1][1].attrib["when"]
                    except : cs_date = "00-00-00"
            
            if  sender == cs_sender and addressee == cs_addressee and place == cs_place and date == cs_date and date != "00-00-00":
                child.set('corresp', record["identifier"][1])

            #elif  sender == cs_sender and addressee == cs_addressee and date == cs_date and date != "00-00-00":
             #   count_place +=1
                #child.set('corresp', record["identifier"][1])
     
    tree.write('app/data/matchs.xml',
           xml_declaration=True,encoding='utf-8',
           method="xml")

    make_cmif('app/data/matchs.xml')