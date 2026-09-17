from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

DB_CONFIG = {
    "host": "college-registration-db.cr8yucsckzil.ap-south-1.rds.amazonaws.com",
    "user": "admin",
    "password": "REDACTED",
    "database": "college_registration",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "RDS CRUD app is live"})

# CREATE
@app.route("/students", methods=["POST"])
def create_student():
    data = request.json
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO students (name, email, phone, major_id) VALUES (%s, %s, %s, %s)",
            (data["name"], data["email"], data.get("phone"), data.get("major_id"))
        )
        conn.commit()
        new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "message": "Student created"}), 201

# READ (all)
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

# READ (one)
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(row)
    return jsonify({"error": "Not found"}), 404

# READ (joined with majors — demonstrates the 2-table relationship)
@app.route("/students-with-majors", methods=["GET"])
def get_students_with_majors():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT students.id, students.name, students.email, majors.major_name, majors.department
            FROM students
            JOIN majors ON students.major_id = majors.id
        """)
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

# UPDATE
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE students SET name=%s, email=%s, phone=%s, major_id=%s WHERE id=%s",
            (data["name"], data["email"], data.get("phone"), data.get("major_id"), student_id)
        )
        conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})

# DELETE
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
