import os
import boto3
import json
import pymysql

# AWS SQS Configuration
QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")

# MySQL Database Configuration
DB_HOST = os.getenv("MYSQL_HOST", "mysql-0.mysql.default.svc.cluster.local")
DB_PORT = int(os.getenv("MYSQL_PORT", 3306))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "rootpassword")
DB_NAME = os.getenv("MYSQL_DATABASE", "messages_db")

# Initialize SQS client
sqs = boto3.client("sqs", region_name=AWS_REGION)

# Function to connect to MySQL
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to insert message into MySQL
def insert_into_db(message):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO messages (event, user_id, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(sql, (message["event"], message["user_id"], message["timestamp"]))
        connection.commit()
        connection.close()
        print("Message inserted into MySQL.")
        return True
    except Exception as e:
        print(f"Error inserting message: {e}")
        return False

# Function to receive messages from SQS and store in MySQL
def receive_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if "Messages" in response:
            for message in response["Messages"]:
                body = json.loads(message["Body"])
                print(f"Received message: {body}")

                # Insert into MySQL
                if insert_into_db(body):
                    # Delete the message after processing
                    sqs.delete_message(
                        QueueUrl=QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    print("Message deleted from queue.")
        else:
            print("No messages available, waiting...")

if __name__ == "__main__":
    receive_messages()
