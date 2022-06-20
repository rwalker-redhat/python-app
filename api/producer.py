import random
from fastapi import APIRouter, HTTPException
from json import dumps
from kafka import KafkaProducer
from environs import Env

# Use environment variables
env = Env()
env.read_env()


router = APIRouter()


@router.get('/kafka/producer')
def producer():
    random_number = random.randint(0, 99)
    producer_data = {'number': random_number}

    try:
        kafka_producer = KafkaProducer(bootstrap_servers=env.list('ENV_BOOTSTRAP_SERVERS'),
                                       value_serializer=lambda x:
                                       dumps(x).encode('utf-8'))
        kafka_producer.send(env.str('ENV_KAFKA_TOPIC'), value=producer_data)
        return {
            'Success adding kafka event': producer_data
        }

    except HTTPException(status_code=400, detail="Bad Request. (Check Kafka is reachable.)"):
        return
