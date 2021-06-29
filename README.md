
# About
This project was developp during my internship at the BBAW in the project ["Travelling Humboldt – Science on the Move"](https://edition-humboldt.de/). 
The purpose of this web app is to enrich the [correspSearch](https://correspsearch.net/) data by indicating the link to the archive document for the correspondence of Alexander von Humboldt.

This app was developed with Flask, an open-source web development framework in Python. For the frond-end, the framework Bootstrap (CSS and HTML) was used.

## Repository`s structure
```
cS-matchingtool
    ├── app
    │   ├── static
    │   │       └── css
    │   │           ├── bootstrap.min.css
    │   │           └── style.css
    │   ├── templates
    │   │       ├── errors/...
    │   │       ├── layout/default.html
    │   │       ├── pages
    │   │       │      ├── download.html
    │   │       │      └── matchingtool.html
    │   │       ├── partials
    │   │       │       ├── css.html
    │   │       │       └── metadata.html
    │   │       └── container.html
    │   ├── utils
    │   │       ├── generic.py
    │   │       └── matching.py
    │   ├── app.py
    │   ├── constantes.py
    │   └── routes.py
    ├── README.md
    ├── requirements.txt
    └── run.py
```
## Features
- The user uploads the CMIF document from correspSearch. 
- It was decided to query Kalliope-Verbund which is probably one of the largest catalogues of archives and libraries in the German-speaking world. The tool developed retrieves data from Kalliope API and searches within it to match the letter corresponding with the one edited and registered on correspSearch.
- Matches considered complete are directly added to the file uploaded by the user. A complete match is based on the GND of the sender, the GND of the receiver, the date of sending and the coverage place.
- Matches for which the location doesn't match must be confirmed (or not) by the user and will then be added to the CMIF file.
- It is possible to upload a CMIF file containing only the complete matches or the user uploaded CMIF file updated with Kalliope links for the matched letters.

# Install and launch the app
## Launch
Prerequisite : python3

_You can install it via this [website](https://www.python.org/downloads/). As a reminder: most Linux systems already have Python installed._ 

### On Linux
#### First Launch
1. Clone this git repository: `git clone https://github.com/axellelecroq/pantheonisees.git` and enter in the folder
2. Install a virtual environnement: `virtualenv -p python3 env`
3. Activate the virtual env via `source env/bin/activate`
4. Install `requirements.txt`: renter in the folder pantheonisees and use this command line `pip install -r requirements.txt`
5. Launch the app : go to the level of `run.py` file and run this command line `python3 run.py`
#### Launch
1. Enter in the app folder
2. Activate the virtualenv: `source env/bin/activate`
3. Launch the app : go to the level of `run.py` gile and run this command line `python3 run.py`


### On Windows