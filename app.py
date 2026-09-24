from flask import Flask, request, render_template, url_for
import gspread
from dotenv import load_dotenv
import json, os, uuid
from google.oauth2.service_account import Credentials

load_dotenv() # loads variables from .env

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Load the string from your environment
creds_env_string = os.environ['GOOGLE_CREDENTIALS']

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

    # 1. Extract first 2 letters of name and surname (uppercase)
    code_nombre = nombre[:2].upper() if len(nombre) >= 2 else nombre.upper().ljust(2, 'X')
    code_apellido = apellido[:2].upper() if len(apellido) >= 2 else apellido.upper().ljust(2, 'X')

    # 2. Extract birth year (assumes input type="date" returning YYYY-MM-DD)
    birth_year = fecha_nacimiento.split("-")[0] if "-" in fecha_nacimiento else fecha_nacimiento[-4:]

    # 3. Concatenate custom ID (e.g., JUAN PEREZ 1995 -> JUPE1995)
    attendee_id = f"{code_nombre}{code_apellido}{birth_year}"
         
    # Append all collected data into Google Sheets
    sheet.append_row([attendee_id, nombre, apellido, fecha_nacimiento, telefono,
                      tipo_miembro, categoria, procedencia, clase])

    return render_template("success.html", attendee_id=attendee_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
