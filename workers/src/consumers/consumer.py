import asyncio
import json
import logging
import os
import sys

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from typing import Optional

sys.path.append(os.path.dirname(__file__) + '/..')

from settings.rabbitmq.config import rabbit_settings  # noqa: E402

from consumer_services.generate_email import generate_email  # noqa: E402
from consumer_services.send_email import EmailSender  # noqa: E402

rabbitmq_settings = rabbit_settings.rabbitmq_settings
logger = logging.getLogger(__name__)


class Handler:

    def __init__(self) -> None:
        self.email_sender: Optional[EmailSender] = None
        self.connection: AbstractRobustConnection

    async def startup(self) -> None:
        self.email_sender = EmailSender()
        self.connection = await self.connect()

    @staticmethod
    async def connect() -> AbstractRobustConnection:
        connection = aio_pika.connect_robust(
            host=rabbitmq_settings.RABBITMQ_HOST,
            port=rabbitmq_settings.RABBITMQ_PORT,
            login=rabbitmq_settings.RABBITMQ_USER,
            password=rabbitmq_settings.RABBITMQ_PASS,
            heartbeat=600,
            blocked_connection_timeout=300,
        )

        return await connection

    async def process_message(
            self, message: aio_pika.abc.AbstractIncomingMessage,
        ) -> None:
        async with message.process():
            body_json = json.loads(message.body.decode('utf-8'))
            generate_email(self.email_sender, message.routing_key, body_json)
            await asyncio.sleep(1)

    async def get_msg(self) -> None:

        async with self.connection:

            channel: aio_pika.abc.AbstractChannel = await self.connection.channel()

            # Declaring queue - to be sure that queue exists
            queue_registration: aio_pika.abc.AbstractQueue = await channel.declare_queue(
                name='registration', durable=True, auto_delete=True,
            )
            queue_admin: aio_pika.abc.AbstractQueue = await channel.declare_queue(
                name='admin_mailing', durable=True, auto_delete=True,
            )

            await queue_registration.consume(self.process_message)
            await queue_admin.consume(self.process_message)

            try:
                # Wait until terminate
                await asyncio.Future()
            finally:
                await self.connection.close()


async def main() -> None:
    handler = Handler()
    await handler.startup()
    await handler.get_msg()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
