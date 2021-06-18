from flask import render_template, flash, request
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
            matching("app/data/records.json")
            flash(
                "All good.",
                category="success",
            )

    return render_template("pages/home.html")


def upload_file(file):
        try:
            file.save(os.path.join(data, secure_filename(file.filename)))
        except Exception as E:
            print(E)
            flash(
                "Error during the upload of the file.",
                category="error",
            )



