
import backoff
import pika
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

    credentials = pika.PlainCredentials(
        rabbitmq_settings.RABBITMQ_USER,
        rabbitmq_settings.RABBITMQ_PASS,
    )
    parameters = pika.ConnectionParameters(
        host=rabbitmq_settings.RABBITMQ_HOST,
        port=rabbitmq_settings.RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError)
    def _connect() -> pika.BlockingConnection:
        return pika.BlockingConnection(parameters=parameters)

    queue_rabbit.connection = _connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    """Shut down settings - disconnect from RabbitMQ"""
    queue_rabbit.connection.close()  # type: ignore


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
