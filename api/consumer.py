from fastapi import APIRouter
from environs import Env
from aiokafka import AIOKafkaConsumer

# Use environment variables
env = Env()
env.read_env()

router = APIRouter()


@router.get('/kafka/consumer')
async def consumer():
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
        # Consume messages
        async for msg in kafka_consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
            return msg.value
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await kafka_consumer.stop()
