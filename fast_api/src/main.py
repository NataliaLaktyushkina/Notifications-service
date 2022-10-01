
import backoff
import pika
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse

from api.v1 import users
from core.config import settings
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
    global connection

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
        blocked_connection_timeout=300
    )

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError)
    def _connect():
        return pika.BlockingConnection(parameters=parameters)

    connection = _connect()
    channel = connection.channel()
    # the producer can only send messages to an exchange.
    # An exchange on one side receives messages from producers
    # and the other side it pushes them to queues.
    # The exchange must know exactly what to do with a message it receives.
    channel.exchange_declare(
        exchange=rabbitmq_settings.RABBITMQ_EXCHANGE,
        exchange_type=rabbitmq_settings.RABBITMQ_EXCHANGE_TYPE,
        durable=True,
    )
    channel.queue_declare(queue=rabbitmq_settings.RABBITMQ_QUEUE_NAME, durable=True)


@app.on_event('shutdown')
async def shutdown() -> None:
    """Shut down settings - disconnect from RabbitMQ"""
    connection.close()


# @app.middleware("http")
# async def before_request(request: Request, call_next):  # type: ignore
#     request_id = request.headers.get('X-Request-Id')
#     if not request_id:
#         raise RuntimeError('request id is required')
#     return await call_next(request)


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
