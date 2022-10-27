
import backoff
import aio_pika
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse

from api.v1 import users
from core.config import settings
from db import queue_rabbit
from services.jwt_check import JWTBearer

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

PROTECTED = [Depends(JWTBearer)]  # noqa: WPS407


@app.on_event('startup')
async def startup() -> None:
    """Start up settings - connect to RabbitMQ"""

    rabbitmq_settings = settings.rabbitmq_settings

    @backoff.on_exception(backoff.expo, aio_pika.exceptions.AMQPConnectionError)
    async def _connect() -> aio_pika.abc.AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host=rabbitmq_settings.RABBITMQ_HOST,
            port=rabbitmq_settings.RABBITMQ_PORT,
            login=rabbitmq_settings.RABBITMQ_USER,
            password=rabbitmq_settings.RABBITMQ_PASS,
            heartbeat=600,
            blocked_connection_timeout=300,
        )

    queue_rabbit.connection = await _connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    """Shut down settings - disconnect from RabbitMQ"""
    await queue_rabbit.connection.close()  # type: ignore


app.include_router(
    users.router, prefix='/api/v1/users',
    tags=['users'], dependencies=PROTECTED,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8101,
    )
#
