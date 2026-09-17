# Lab 5 — Assignment 2: DynamoDB Integration

## Overview
A Flask REST API deployed on Amazon EC2, connected to a DynamoDB table using an IAM role (no hardcoded AWS credentials). Demonstrates full CRUD operations with 5 distinct DynamoDB attribute types.

## Architecture
```
Internet → EC2 Security Group (port 8080) → EC2 instance (Flask app, boto3 SDK)
                                                      ↓
                                        IAM Role (EC2-DynamoDB-Role)
                                                      ↓
                                          Amazon DynamoDB (Students table)
```

## Database Deployment Steps
1. Created a DynamoDB table named `Students`
2. Partition key: `student_id` (String)
3. No sort key used
4. Default table settings (on-demand capacity)

## IAM Role Setup (No Hardcoded Keys)
1. Created an IAM role `EC2-DynamoDB-Role` with the `AmazonDynamoDBFullAccess` policy
2. Attached the role directly to the EC2 instance via **Actions → Security → Modify IAM role**
3. The application uses `boto3.resource('dynamodb')`, which automatically picks up credentials from the instance's attached IAM role — no access keys are stored in code or environment variables

## Datatypes Demonstrated (5 required)
| Attribute | DynamoDB Type | Example |
|---|---|---|
| `student_id` | String (S) | `"S001"` |
| `name` | String (S) | `"Priya Sharma"` |
| `age` | Number (N) | `20` |
| `is_active` | Boolean (BOOL) | `true` |
| `subjects` | List (L) | `["Math", "Cloud Computing"]` |
| `address` | Map (M) | `{"city": "Mumbai", "pincode": "400050"}` |

## API Endpoints (CRUD)
| Method | Endpoint | Operation |
|---|---|---|
| POST | `/students` | Create |
| GET | `/students` | Read (all) |
| GET | `/students/<student_id>` | Read (one) |
| PUT | `/students/<student_id>` | Update |
| DELETE | `/students/<student_id>` | Delete |

## EC2 URL
`http://<ec2-public-ip>:8080`

## Security
- Access to DynamoDB is exclusively via the attached IAM role
- No AWS access keys/secret keys present anywhere in the codebase
- Deployed as a systemd service (`dynamo-crud.service`) for persistence

## Running Locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask boto3
python app.py
```
