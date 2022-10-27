from typing import Optional

from aio_pika import RobustConnection

connection: Optional[RobustConnection]= None


async def get_connection() -> RobustConnection:
    return connection
