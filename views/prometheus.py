import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from prometheus_client import Counter

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')

# Custom Metric
counter = Counter('arbitrary_counter', 'number of times button clicked')


def increment_counter():
    counter.inc()


def get_current_counter_value():
    return counter._value.get()


@router.get('/prometheus')
def prometheus_page(request: Request):
    value = get_current_counter_value()
    return templates.TemplateResponse('prometheus.html', {'request': request, 'value': value})


@router.post('/prometheus')
def prometheus_page(request: Request):
    increment_counter()
    value = get_current_counter_value()
    return templates.TemplateResponse('prometheus.html', {'request': request, 'value': value})
