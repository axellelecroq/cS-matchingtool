from flask import render_template, flash, request, send_file, redirect
import xml.etree.ElementTree as ET
import json

from ..app import *
from ..utils.matching import matching
from ..utils.generic  import upload_file, count_corresp


"""
/
/download
/about
"""

@app.route("/", methods=["GET", "POST"])
def handle_matching():
    print(request.form)
    print(request.method)
    if request.method.lower() == "post" and 'upload' in request.form:
        if request.files["records"]:
            file = request.files["records"]
            upload_file(file)
            possibles = matching("app/data/{filename}".format(filename=file.filename))
            count = count_corresp("app/data/matchs.xml")
            return render_template("pages/matchingtool.html", uploaded = True, matchs = possibles, count_fullmatchs = count)
    elif request.method.lower() == "post" and 'fullMatchs' in request.form:
        return send_file("app/data/matchs.xml", as_attachment=True, attachment_filename="matchs.xml")
        
    return render_template("pages/matchingtool.html", uploaded= False)


@app.route("/download", methods=["GET", "POST"])
def save_file():
    if request.method.lower() == "post" and 'downloadOnly' in request.form:
        return send_file("app/data/output.xml", as_attachment=True, attachment_filename="output.xml")
        
    elif request.method.lower() == "post" and 'downloadAll' in request.form:
            return send_file("app/data/output.xml", as_attachment=True, attachment_filename="matchs.xml")

    return render_template("pages/download.html")


@app.route('/about')
def about():
    return render_template('pages/about.html')