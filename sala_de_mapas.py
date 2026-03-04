from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE CLOUDINARY (Imágenes) ---
cloudinary.config(
    cloud_name = "dqqnfpnjt",
    api_key = "247744316653339",
    api_secret = "TgSyz4lcoXfRfZ5yF0s97qf1lEY",
    secure = True
)

# --- 2. CONFIGURACIÓN DE MONGODB ATLAS (Datos y Niebla) ---
MONGO_URI = "mongodb+srv://dm_tabernero:rcoY8Ynqjtznabh5@lodte.ylvopii.mongodb.net/?retryWrites=true&w=majority&appName=LODTE"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client['sala_de_mapas']
coleccion_mapas = db['mapas_metadata']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('mapa.html')

# Ruta para servir la imagen de fondo de la taberna (sigue siendo local)
@app.route('/assets/<path:filename>')
def servir_assets(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route('/api/mapas', methods=['GET'])
def obtener_estructura_mapas():
    # En vez de leer carpetas, ahora le preguntamos a la Base de Datos qué mapas existen
    mapas_db = coleccion_mapas.find({}, {"_id": 0, "campaign": 1, "mapName": 1, "imagePath": 1})
    estructura = {}
    
    for mapa in mapas_db:
        campana = mapa.get("campaign", "Sin Campaña")
        if campana not in estructura:
            estructura[campana] = []
            
        estructura[campana].append({
            "nombre_mapa": mapa.get("mapName", "Sin Nombre"),
            "ruta_relativa": mapa.get("imagePath", "") # Ahora esto es un link a Cloudinary
        })

    return jsonify(estructura)

@app.route('/api/upload', methods=['POST'])
def subir_mapa():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se seleccionó ninguna imagen."}), 400
    
    archivo = request.files['imagen']
    campana = request.form.get('campana', 'Sin Campaña').strip()
    mapa_nombre = request.form.get('mapa', 'Sin Nombre').strip()
    grid_size = request.form.get('gridSize', 40)
    
    if archivo.filename == '':
        return jsonify({"error": "Archivo inválido."}), 400

    try:
        # 1. Subir la imagen a Cloudinary
        carpeta_destino = f"SalaDeMapas/{secure_filename(campana)}"
        respuesta_cloud = cloudinary.uploader.upload(
            archivo, 
            folder=carpeta_destino,
            public_id=secure_filename(mapa_nombre)
        )
        url_imagen = respuesta_cloud.get("secure_url")

        # 2. Crear el registro base en MongoDB
        filtro = {"campaign": campana, "mapName": mapa_nombre}
        actualizacion = {
            "$set": {
                "campaign": campana,
                "mapName": mapa_nombre,
                "imagePath": url_imagen,
                "gridSize": int(grid_size)
            },
            # Si el mapa es nuevo, creamos los arrays vacíos. Si ya existía, no pisamos la niebla vieja.
            "$setOnInsert": {
                "gridState": {},
                "pois": []
            }
        }
        coleccion_mapas.update_one(filtro, actualizacion, upsert=True)

        return jsonify({"success": True, "ruta": url_imagen})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save', methods=['POST'])
def guardar_metadata():
    data = request.json
    campana = data.get('campaign')
    mapa_nombre = data.get('mapName')

    if not campana or not mapa_nombre:
        return jsonify({"error": "Faltan datos de campaña o mapa"}), 400

    try:
        # Guardamos TODO el JSON directo en MongoDB Atlas
        filtro = {"campaign": campana, "mapName": mapa_nombre}
        actualizacion = {"$set": data}
        coleccion_mapas.update_one(filtro, actualizacion, upsert=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/load', methods=['GET'])
def cargar_metadata():
    campana = request.args.get('campana')
    mapa_nombre = request.args.get('mapa')

    if not campana or not mapa_nombre:
        return jsonify({"error": "Faltan parámetros"}), 400

    # Buscamos en la nube
    mapa_db = coleccion_mapas.find_one({"campaign": campana, "mapName": mapa_nombre}, {"_id": 0})

    if mapa_db:
        return jsonify(mapa_db)
    else:
        return jsonify({"empty": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)