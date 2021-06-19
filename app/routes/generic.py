from flask import render_template, flash, request, send_file, redirect
from werkzeug.utils import secure_filename
from ..app import *
from ..routes.matching import matching

import xml.etree.ElementTree as ET
import json


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method.lower() == "post":
        if request.files["records"]:
            records = request.files["records"]
            records.filename = "records.json"
            upload_file(records)
            #matching("app/data/records.json")
            return redirect('/download')
        
    return render_template("pages/home.html")

@app.route("/download", methods=["GET", "POST"])
def save_file():
    if request.method.lower() == "post":
        #return send_file("app/data/output.xml")
        #print("ok")
        return send_file("app/data/output.xml", as_attachment=True, attachment_filename="matchs.xml")
    return render_template("pages/download.html")
    



def upload_file(file):
        try:
            file.save(os.path.join(data, secure_filename(file.filename)))
        except Exception as E:
            print(E)
            flash(
                "Error during the upload of the file.",
                category="error",
            )



