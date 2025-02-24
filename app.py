from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://alumnos_8rbt_user:iiHLa0nbCEYfrGnHRrOeTn2WNVmQ1BkO@dpg-cuufrfdsvqrc73dlbv10-a.oregon-postgres.render.com/alumnos_8rbt"

# Función para conectar a la BD
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# 🔹 Endpoint para obtener todos los alumnos
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos;")
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertir a JSON
    alumnos_list = [
        {
            "id": row[0],
            "no_control": row[1],
            "nombre": row[2],
            "ape_P": row[3],
            "ape_M": row[4],
            "edad": row[5],
            "promedio_global": float(row[6]),
            "semestre": row[7]
        }
        for row in alumnos
    ]
    return jsonify(alumnos_list)

# 🔹 Endpoint para obtener un alumno por ID
@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos WHERE id = %s;", (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Alumno no encontrado"}), 404

    alumno = {
        "id": row[0],
        "no_control": row[1],
        "nombre": row[2],
        "ape_P": row[3],
        "ape_M": row[4],
        "edad": row[5],
        "promedio_global": float(row[6]),
        "semestre": row[7]
    }
    return jsonify(alumno)

# 🔹 Endpoint para agregar un nuevo alumno


if __name__ == '__main__':
    app.run(debug=True)
