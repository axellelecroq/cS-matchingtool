from flask import render_template, flash, request, send_file, redirect
import xml.etree.ElementTree as ET
import json

from ..app import *
from ..utils.matching import matching
from ..utils.generic  import upload_file

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route("/matching", methods=["GET", "POST"])
def handle_matching():
    if request.method.lower() == "post" and 'upload' in request.form:
        if request.files["records"]:
            file = request.files["records"]
            upload_file(file)
            matching("app/data/{filename}".format(filename=file.filename))
            return render_template("pages/matchingtool.html", download= True)

    elif request.method.lower() == "post" and 'download' in request.form:
        print('ok')
        return send_file("app/data/output.xml", as_attachment=True, attachment_filename="matchs.xml")
        
    return render_template("pages/matchingtool.html", download= False)

