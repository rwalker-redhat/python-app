import random
from fastapi import HTTPException, status, Form
import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from environs import Env
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi.encoders import jsonable_encoder

# Use environment variables
env = Env()
env.read_env()

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')


@router.get('/kafka')
def kafka_page(request: Request):
    context = {
        'page': 'Kafka'
    }
    return templates.TemplateResponse('kafka.html', {'request': request, 'context': context})


# POST
async def kafka_consume_or_500():

    try:
        kafka_consumer = AIOKafkaConsumer(env.str('ENV_KAFKA_TOPIC'),
                                          bootstrap_servers=env.list('ENV_BOOTSTRAP_SERVERS'),
                                          group_id="example",
                                          enable_auto_commit=True,
                                          auto_commit_interval_ms=1000,
                                          auto_offset_reset="earliest",
                                          request_timeout_ms=5000,
                                          consumer_timeout_ms=5000)

        await kafka_consumer.start()

        try:
            async for msg in kafka_consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
                return msg.value

        finally:
            await kafka_consumer.stop()
            return msg.value

    except (RuntimeError, TypeError, NameError, KeyError):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def kafka_produce_or_500():
    random_number = random.randint(0, 99)

    try:
        kafka_producer = AIOKafkaProducer(bootstrap_servers=env.list('ENV_BOOTSTRAP_SERVERS'))

        await kafka_producer.start()

        try:
            await kafka_producer.send_and_wait(env.str('ENV_KAFKA_TOPIC'), bytes(str(random_number), encoding='utf-8'))
            return bytes(str(random_number), encoding='utf-8')
        finally:
            await kafka_producer.stop()
            return bytes(str(random_number), encoding='utf-8')

    except (RuntimeError, TypeError, NameError, KeyError):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/producer')
async def kafka_page(request: Request, producer_action: str = Form()):

    event = await kafka_produce_or_500()
    json_compatible_item_data = jsonable_encoder(event)

    context = {
        'page': 'kafka',
        'produce_event': json_compatible_item_data
    }

    return templates.TemplateResponse('kafka.html', {'request': request, 'context': context})


@router.post('/consumer')
async def kafka_page(request: Request, consumer_action: str = Form()):

    event = await kafka_consume_or_500()
    json_compatible_item_data = jsonable_encoder(event)

    context = {
        'page': 'kafka',
        'consume_event': json_compatible_item_data
    }

    return templates.TemplateResponse('kafka.html', {'request': request, 'context': context})
