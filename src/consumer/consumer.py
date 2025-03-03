import os
import boto3
import json

# AWS SQS Configuration
QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Initialize SQS client
sqs = boto3.client("sqs")

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
