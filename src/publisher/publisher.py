import os
import boto3
import json
import uuid

# AWS SQS Configuration
QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Initialize SQS client
sqs = boto3.client("sqs")

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

    print("Messages sent successfully!")
    if "Successful" in response:
        for msg in response["Successful"]:
            print(f"MessageId: {msg['MessageId']} sent successfully.")
    if "Failed" in response:
        for msg in response["Failed"]:
            print(f"MessageId: {msg['Id']} failed with error: {msg['Message']}")


if __name__ == "__main__":
    messages = [
        {"event": "user_signup", "user_id": 101, "timestamp": "2025-03-03T12:00:00Z"},
        {"event": "order_placed", "order_id": 202, "amount": 150.5, "timestamp": "2025-03-03T12:05:00Z"},
        {"event": "user_logout", "user_id": 303, "timestamp": "2025-03-03T12:10:00Z"}
    ]

    send_messages(messages)
