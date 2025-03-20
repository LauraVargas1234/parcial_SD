from flask import Flask, jsonify
from neo4j import GraphDatabase
import psycopg2
import csv
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

neo4j_driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

def get_postgres_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="postgres"
    )

def extract_data():
    with neo4j_driver.session() as session:
        result = session.run("MATCH (p:Pelicula) RETURN p")
        data = [dict(record['p']) for record in result]
    return data

def transform_data(data):
    transformed = []
    for movie in data:
        nombre_formateado = movie['nombre'].lower().replace(' ', '-')
        
        calificacion = movie['calificacion']
        if calificacion <= 5:
            categoria_calificacion = "Mala"
        elif 5 < calificacion <= 7:
            categoria_calificacion = "Regular"
        else:
            categoria_calificacion = "Buena"
        
        año = movie['año_lanzamiento']
        decada = f"{str(año)[:3]}0s"
        
        puntuacion_ajustada = (calificacion * 2) - (2025 - año) / 10
        
        transformed.append({
            "id": movie['id'],
            "nombre_formateado": nombre_formateado,
            "categoria_calificacion": categoria_calificacion,
            "decada": decada,
            "puntuacion_ajustada": puntuacion_ajustada,
            "fecha_procesamiento": datetime.now().strftime("%Y-%m-%d")
        })
    return transformed

def load_data(data):
    conn = get_postgres_connection()
    cur = conn.cursor()
    for item in data:
        cur.execute("""
            INSERT INTO etl_data (id, nombre_formateado, categoria_calificacion, decada, puntuacion_ajustada, fecha_procesamiento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item['id'],
            item['nombre_formateado'],
            item['categoria_calificacion'],
            item['decada'],
            item['puntuacion_ajustada'],
            item['fecha_procesamiento']
        ))
    conn.commit()
    cur.close()
    conn.close()

def export_to_csv():
    conn = get_postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM etl_data")
    rows = cur.fetchall()
    
    with open('recap.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'nombre_formateado', 'categoria_calificacion', 'decada', 'puntuacion_ajustada', 'fecha_procesamiento'])
        writer.writerows(rows)
    
    cur.close()
    conn.close()

@app.route('/api/extract', methods=['GET'])
def extract():
    try:
        data = extract_data()
        if not data:
            return jsonify({"error": "Informacion no encontrada en Neo4j"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/etl', methods=['GET'])
def run_etl():
    try:
        raw_data = extract_data()
        if not raw_data:
            return jsonify({"error": "Informacion no encontrada en Neo4j"}), 404

        transformed_data = transform_data(raw_data)
        if not transformed_data:
            return jsonify({"error": "La transformacion no fue completada"}), 500

        load_data(transformed_data)

        export_to_csv()

        return jsonify({"message": "Tranformacion terminada exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)