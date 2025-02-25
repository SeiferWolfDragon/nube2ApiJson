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
# 🔹 Endpoint para agregar un nuevo alumno
@app.route('/alumnos', methods=['POST'])
def create_alumno():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alumnos (no_control, nombre, ape_P, ape_M, edad, promedio_global, semestre) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
            (data['no_control'], data['nombre'], data['ape_P'], data['ape_M'], data['edad'], data['promedio_global'], data['semestre'])
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"id": new_id, "message": "Alumno creado"}), 201
    except psycopg2.Error as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": "Faltan datos en la solicitud", "missing_field": str(e)}), 400
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# 🔹 Endpoint para actualizar un alumno
@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    try:
        data = request.json
        required_fields = ["no_control", "nombre", "ape_P", "ape_M", "edad", "promedio_global", "semestre"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": "Faltan datos", "missing_fields": missing_fields}), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE alumnos SET no_control=%s, nombre=%s, ape_P=%s, ape_M=%s, edad=%s, promedio_global=%s, semestre=%s WHERE id=%s RETURNING id;",
                    (data['no_control'], data['nombre'], data['ape_P'], data['ape_M'], data['edad'], data['promedio_global'], data['semestre'], id)
                )
                updated = cursor.fetchone()
                if updated is None:
                    return jsonify({"error": "Alumno no encontrado"}), 404
        return jsonify({"message": "Alumno actualizado"})
    except psycopg2.Error as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
