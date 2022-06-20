import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')


@router.get('/')
def home_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
