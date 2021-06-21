from flask import render_template, flash, request, send_file, redirect
import xml.etree.ElementTree as ET
import json

from ..app import *
from ..utils.matching import matching
from ..utils.generic  import upload_file




@app.route("/", methods=["GET", "POST"])
def home():
    if request.method.lower() == "post":
        if request.files["records"]:
            records = request.files["records"]
            records.filename = "records.json"
            upload_file(records)
            matching("app/data/records.json")
            return redirect('/download')
        
    return render_template("pages/home.html")


@app.route("/download", methods=["GET", "POST"])
def save_file():
    if request.method.lower() == "post":
        return send_file("app/data/output.xml", as_attachment=True, attachment_filename="matchs.xml")
    return render_template("pages/download.html")
