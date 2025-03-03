import boto3
import json

# AWS SQS Configuration
QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/YOUR_ACCOUNT_ID/YOUR_QUEUE_NAME"

# Initialize SQS client
sqs = boto3.client("sqs")

def send_message(message_body):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )
    print(f"Message sent! MessageId: {response['MessageId']}")

if __name__ == "__main__":
    message = {"event": "user_signup", "user_id": 123, "timestamp": "2025-03-03T12:00:00Z"}
    send_message(message)
