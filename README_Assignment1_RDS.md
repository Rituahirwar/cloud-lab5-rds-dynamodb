# Lab 5 — Assignment 1: RDS MySQL Integration

## Overview
A Flask REST API deployed on Amazon EC2, connected to a MySQL database hosted on Amazon RDS. Demonstrates full CRUD operations against two related tables (`students` and `majors`).

## Architecture
```
Internet → EC2 Security Group (port 80) → EC2 instance (Flask app)
                                                   ↓
                                    RDS Security Group (port 3306, source = EC2 SG only)
                                                   ↓
                                        Amazon RDS MySQL (college_registration DB)
```

## Database Deployment Steps
1. Created an Amazon RDS MySQL instance (`db.t3.micro`, Free Tier template, Single-AZ)
2. Initial database name: `college_registration`
3. Created a dedicated security group (`rds-mysql-sg`) restricting inbound port 3306 access to **only** the EC2 instance's security group (`rds-crud-ec2-sg`) — no `0.0.0.0/0` access
4. Connected via MySQL client and created two related tables:
   - `majors` (id, major_name, department)
   - `students` (id, name, email, phone, major_id → foreign key to majors.id)

## Connection Steps
The Flask app (`app.py`) connects to RDS using `pymysql`:
```python
DB_CONFIG = {
    "host": "<rds-endpoint>",
    "user": "admin",
    "password": "<redacted>",
    "database": "college_registration"
}
```

## API Endpoints (CRUD)
| Method | Endpoint | Operation |
|---|---|---|
| POST | `/students` | Create |
| GET | `/students` | Read (all) |
| GET | `/students/<id>` | Read (one) |
| PUT | `/students/<id>` | Update |
| DELETE | `/students/<id>` | Delete |
| GET | `/students-with-majors` | Read (joined relationship) |

## EC2 URL
`http://<ec2-public-ip>`

## Security
- RDS inbound rule: MySQL/Aurora (3306), Source = EC2 security group ID only
- No public (0.0.0.0/0) database access
- Deployed as a systemd service (`rds-crud.service`) for persistence across reboots

## Running Locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask pymysql
python app.py
```
