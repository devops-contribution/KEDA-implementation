import os
import boto3
import json
import uuid

# AWS SQS Configuration
QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")

# Initialize SQS client
sqs = boto3.client("sqs", region_name=AWS_REGION)

def send_messages(messages):
    entries = [
        {
            "Id": str(uuid.uuid4()),  # Unique ID per message
            "MessageBody": json.dumps(msg)
        }
        for msg in messages
    ]

    response = sqs.send_message_batch(
        QueueUrl=QUEUE_URL,
        Entries=entries
    )

    # print("Messages sent successfully!")
    if "Successful" in response:
        for msg in response["Successful"]:
            print(f"MessageId: {msg['MessageId']} sent successfully.")
    if "Failed" in response:
        for msg in response["Failed"]:
            print(f"MessageId: {msg['Id']} failed with error: {msg['Message']}")


if __name__ == "__main__":
    messages = [
        {"event": "user_signup", "user_id": 101, "timestamp": "2025-03-03 12:00:00"},
        {"event": "order_placed", "order_id": 202, "amount": 150.5, "timestamp": "2025-03-03 12:00:10"},
        {"event": "user_logout", "user_id": 303, "timestamp": "2025-03-03 12:00:20"},
        {"event": "password_reset", "user_id": 405, "timestamp": "2025-03-03 12:00:30"},
        {"event": "order_placed", "order_id": 207, "amount": 275.3, "timestamp": "2025-03-03 12:00:40"},
        {"event": "user_signup", "user_id": 502, "timestamp": "2025-03-03 12:00:50"},
        {"event": "profile_update", "user_id": 603, "timestamp": "2025-03-03 12:01:00"},
        {"event": "order_placed", "order_id": 208, "amount": 99.9, "timestamp": "2025-03-03 12:01:10"},
        {"event": "user_logout", "user_id": 704, "timestamp": "2025-03-03 12:01:20"},
        {"event": "password_reset", "user_id": 805, "timestamp": "2025-03-03 12:01:30"},
    #    {"event": "user_signup", "user_id": 906, "timestamp": "2025-03-03 12:01:40"},
    #    {"event": "order_placed", "order_id": 209, "amount": 300.0, "timestamp": "2025-03-03 12:01:50"},
    #    {"event": "profile_update", "user_id": 1007, "timestamp": "2025-03-03 12:02:00"},
    #    {"event": "user_logout", "user_id": 1108, "timestamp": "2025-03-03 12:02:10"},
    #    {"event": "order_placed", "order_id": 210, "amount": 450.25, "timestamp": "2025-03-03 12:02:20"},
    #    {"event": "user_signup", "user_id": 1209, "timestamp": "2025-03-03 12:02:30"},
    #    {"event": "password_reset", "user_id": 1310, "timestamp": "2025-03-03 12:02:40"},
    #    {"event": "order_placed", "order_id": 211, "amount": 175.75, "timestamp": "2025-03-03 12:02:50"},
    #    {"event": "user_logout", "user_id": 1411, "timestamp": "2025-03-03 12:03:00"},
    #    {"event": "profile_update", "user_id": 1512, "timestamp": "2025-03-03 12:03:10"},
    #    {"event": "user_signup", "user_id": 1613, "timestamp": "2025-03-03 12:03:20"},
    #    {"event": "order_placed", "order_id": 212, "amount": 99.99, "timestamp": "2025-03-03 12:03:30"},
    #    {"event": "user_logout", "user_id": 1714, "timestamp": "2025-03-03 12:03:40"},
    #    {"event": "password_reset", "user_id": 1815, "timestamp": "2025-03-03 12:03:50"},
    #    {"event": "order_placed", "order_id": 213, "amount": 275.00, "timestamp": "2025-03-03 12:04:00"},
    #    {"event": "profile_update", "user_id": 1916, "timestamp": "2025-03-03 12:04:10"},
    #    {"event": "user_signup", "user_id": 2017, "timestamp": "2025-03-03 12:04:20"},
    #    {"event": "order_placed", "order_id": 214, "amount": 320.40, "timestamp": "2025-03-03 12:04:30"},
    #    {"event": "user_logout", "user_id": 2118, "timestamp": "2025-03-03 12:04:40"},
    #    {"event": "password_reset", "user_id": 2219, "timestamp": "2025-03-03 12:04:50"},
    #    {"event": "order_placed", "order_id": 215, "amount": 199.99, "timestamp": "2025-03-03 12:05:00"},
    #    {"event": "profile_update", "user_id": 2320, "timestamp": "2025-03-03 12:05:10"},
    #    {"event": "user_signup", "user_id": 2421, "timestamp": "2025-03-03 12:05:20"}
    ]

    send_messages(messages)
