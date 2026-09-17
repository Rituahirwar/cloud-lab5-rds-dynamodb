from flask import Flask, request, jsonify
import boto3
from decimal import Decimal

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('Students')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "DynamoDB CRUD app is live"})

# CREATE
@app.route("/students", methods=["POST"])
def create_student():
    data = request.json
    item = {
        "student_id": data["student_id"],                 # String (S)
        "name": data["name"],                              # String (S)
        "age": data.get("age", 20),                        # Number (N)
        "is_active": data.get("is_active", True),          # Boolean (BOOL)
        "subjects": data.get("subjects", ["Math", "CS"]),  # List (L)
        "address": data.get("address", {                   # Map (M)
            "city": "Mumbai",
            "pincode": "400050"
        })
    }
    table.put_item(Item=item)
    return jsonify({"message": "Student created", "item": item}), 201

# READ (all)
@app.route("/students", methods=["GET"])
def get_students():
    response = table.scan()
    items = response.get("Items", [])
    return app.response_class(
        response=jsonify(items).get_data(),
        mimetype='application/json'
    )

# READ (one)
@app.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    response = table.get_item(Key={"student_id": student_id})
    item = response.get("Item")
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

# UPDATE
@app.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    table.update_item(
        Key={"student_id": student_id},
        UpdateExpression="SET #n = :name, age = :age, is_active = :active",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={
            ":name": data.get("name", "Unknown"),
            ":age": data.get("age", 21),
            ":active": data.get("is_active", True)
        }
    )
    return jsonify({"message": "Student updated"})

# DELETE
@app.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    table.delete_item(Key={"student_id": student_id})
    return jsonify({"message": "Student deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
