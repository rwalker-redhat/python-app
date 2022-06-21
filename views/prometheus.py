import fastapi
from fastapi import Form
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from prometheus_client import Counter, Gauge

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')

# Custom Metric
counter = Gauge('arbitrary_counter', 'number of times button clicked')


def increment_counter():
    counter.inc()


def decrease_counter():
    counter.dec()


def get_current_counter_value():
    return counter._value.get()


@router.get('/prometheus')
def prometheus_page(request: Request):
    value = get_current_counter_value()
    return templates.TemplateResponse('prometheus.html', {'request': request, 'value': value})


@router.post('/prometheus')
def prometheus_page(request: Request, action: str = Form()):
    if action == "increment":
        increment_counter()
    if action == "decrease":
        decrease_counter()
    value = get_current_counter_value()
    return templates.TemplateResponse('prometheus.html', {'request': request, 'value': value})
