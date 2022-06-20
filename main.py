from fastapi import FastAPI
import uvicorn
from api import pets, health, hashgen, producer, consumer
from api.warner import warner
from views import home, apis, kafka, prometheus
from starlette.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

main_app = FastAPI()

# Prometheus
Instrumentator().instrument(main_app).expose(main_app)


def configure():
    configure_routing()


def configure_routing():
    main_app.mount('/static', StaticFiles(directory='static'), name='static')

    # APIs
    main_app.include_router(pets.router)
    main_app.include_router(warner.router)
    main_app.include_router(health.router)
    main_app.include_router(hashgen.router)
    main_app.include_router(producer.router)
    main_app.include_router(consumer.router)

    # Pages
    main_app.include_router(home.router)
    main_app.include_router(apis.router)
    main_app.include_router(kafka.router)
    main_app.include_router(prometheus.router)


if __name__ == '__main__':
    configure()
    uvicorn.run(main_app, host='0.0.0.0', port=8000)
else:
    configure()
