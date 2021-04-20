from __future__ import annotations

import asyncio
import sys

import aiobotocore
import botocore

QUEUE_NAME = "async_test"
SERVICE_NAME = "sqs"
REGION_NAME = "ap-southeast-1"
MAX_CONSUMERS = 2


async def send_message(
    msg_body: str,
    queue_name: str,
    service_name: str,
    region_name: str,
) -> None:

    # Boto should get credentials from ~/.aws/credentials or the environment.
    session = aiobotocore.get_session()
    async with session.create_client(service_name, region_name=region_name) as client:
        try:
            response = await client.get_queue_url(QueueName=queue_name)
        except botocore.exceptions.ClientError as err:
            if (
                err.response["Error"]["Code"]
                == "AWS.SimpleQueueService.NonExistentQueue"
            ):
                print(f"Queue {queue_name} does not exist")
                sys.exit(1)
            else:
                raise

        queue_url = response["QueueUrl"]

        print("Putting messages on the queue")

        msg_no = 1
        while True:
            msg = f"{msg_no}_{msg_body}"
            await client.send_message(QueueUrl=queue_url, MessageBody=msg)
            msg_no += 1

            print(f'Pushed "{msg}" to queue')

            await asyncio.sleep(2)
            if msg_no == 5:
                break

        print("Finished")


async def receive_message(queue_name: str, service_name: str, region_name: str):
    # Boto should get credentials from ~/.aws/credentials or the environment.
    session = aiobotocore.get_session()
    async with session.create_client(service_name, region_name=region_name) as client:
        try:
            response = await client.get_queue_url(QueueName=queue_name)
        except botocore.exceptions.ClientError as err:
            if (
                err.response["Error"]["Code"]
                == "AWS.SimpleQueueService.NonExistentQueue"
            ):
                print(f"Queue {queue_name} does not exist.")
                sys.exit(1)
            else:
                raise

        queue_url = response["QueueUrl"]

        print("Pulling messages off the queue")

        while True:
            # This loop wont spin really fast as there is
            # essentially a sleep in the receive_message call.
            response = await client.receive_message(
                QueueUrl=queue_url,
                WaitTimeSeconds=5,
            )

            if "Messages" in response:
                for msg in response["Messages"]:
                    print(f'Got msg "{msg["Body"]}"')
                    # Need to remove msg from queue or else it'll reappear.
                    await client.delete_message(
                        QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"]
                    )
            else:
                print("No messages in queue")
                break
        print("Finished")


async def main():
    producer_task = asyncio.create_task(
        send_message(
            msg_body="hello world",
            queue_name=QUEUE_NAME,
            service_name=SERVICE_NAME,
            region_name=REGION_NAME,
        )
    )

    consumer_tasks = [
        asyncio.create_task(
            receive_message(
                queue_name=QUEUE_NAME,
                service_name=SERVICE_NAME,
                region_name=REGION_NAME,
            )
        )
        for _ in range(MAX_CONSUMERS)
    ]
    consumer_tasks.append(producer_task)

    await asyncio.gather(*consumer_tasks)


if __name__ == "__main__":
    asyncio.run(main())
