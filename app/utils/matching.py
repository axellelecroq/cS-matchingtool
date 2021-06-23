
import xml.etree.ElementTree as ET
import json
import requests

from .generic import make_cmif

def matching(file: str):
    tree = ET.parse(file)
    root_cs = tree.getroot()
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

    possibles = {}
    count = 0 

    # ---- Kalliope
    kalliope_links = ["https://kalliope-verbund.info/sru?version=1.2&operation=searchRetrieve&query=ead.addressee.gnd%3D%3D%22118554700%22+AND+ead.genre%3D%3D%22Brief%22&maximumRecords=5000&recordSchema=mods", "https://kalliope-verbund.info/sru?version=1.2&operation=searchRetrieve&query=ead.creator.gnd%3D%3D%22118554700%22+AND+ead.genre%3D%3D%22Brief%22&maximumRecords=5000&recordSchema=mods"]

    for request in kalliope_links:
        root_k = ET.fromstring(requests.get(request).content)
        for record in root_k[2]:
            date = ''
            place = ''
            for recordInfo in record[2][0]: 
                # Kalliope link / identifier
                if recordInfo.tag == '{http://www.loc.gov/mods/v3}identifier':
                    identifier = recordInfo.text
        
                # Addressee and sender
                for person in recordInfo.iter('{http://www.loc.gov/mods/v3}name'):
                    for role in person.find('{http://www.loc.gov/mods/v3}role'):
                        if role.text == 'addressee':
                            try:
                                addr_uri = person.attrib['valueURI']
                            except : addr_uri = ''
                        if role.text == 'author':
                            try:
                                auth_uri = person.attrib['valueURI']
                            except : auth_uri = ''
        
                # Coverage place
                for place in recordInfo.findall('.//{http://www.loc.gov/mods/v3}placeTerm'):
                    place = place.text
                    if '[' in place :
                        place = place.split(' [')[0]
                    elif '(' in place :
                        place = place.split(' (')[0]
                # Date
                for date in recordInfo.findall('.//{http://www.loc.gov/mods/v3}dateCreated'):
                    date = date.text

        # ---- correspSearch
            for child in root_cs[0][1]:
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
            
                if  auth_uri == cs_sender and addr_uri == cs_addressee and date == cs_date and date != "00-00-00" and place == cs_place:
                    child.set('corresp', identifier)
                elif  auth_uri == cs_sender and addr_uri == cs_addressee and date == cs_date and date != "00-00-00" :
                    possibles[count]= [[auth_uri, cs_sender], [addr_uri, cs_addressee], [date, cs_date], [place, cs_place], identifier]
                    count +=1
     
    tree.write('app/data/matchs.xml',
           xml_declaration=True,encoding='utf-8',
           method="xml")
    
    return possibles

    #make_cmif('app/data/matchs.xml')

