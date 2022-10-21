from typing import Optional

from pika import BlockingConnection

connection: Optional[BlockingConnection]= None


async def get_connection() -> BlockingConnection:
    return connection
