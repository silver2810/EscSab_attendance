from flask import Flask, request, render_template, url_for
import gspread
from dotenv import load_dotenv
import json, os
from google.oauth2.service_account import Credentials

load_dotenv() # loads variables from .env

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Load the string from your environment
creds_env_string = os.environ['GOOGLE_CREDENTIALS']

# Remove carriage returns and literal newlines
#creds_env_string = ''.join(ch for ch in creds_env_string if ord(ch) >= 32 or ch in ['\\', '"'])

# Parse it into a dictionary
creds_dict = json.loads(creds_env_string)

# Authenticate using the modern method
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("Registro_ES_Galilea_2026").sheet1

# --- Flask app setup ---
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")   # <-- loads your external file

@app.route("/submit", methods=["POST"])
def submit():
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    fecha_nacimiento = request.form.get("fecha_nacimiento")
    telefono = request.form.get("telefono")
    tipo_miembro = request.form.get("tipo_miembro")
    categoria = request.form.get("categoria")
    procedencia = request.form.get("procedencia")
    clase = request.form.get("clase")

    # Append all collected data into Google Sheets
    sheet.append_row([nombre, apellido, fecha_nacimiento, telefono,
                      tipo_miembro, categoria, procedencia, clase])

    return render_template("success.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
