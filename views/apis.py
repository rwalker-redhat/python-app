import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')


@router.get('/apis')
def apis_page(request: Request):
    return templates.TemplateResponse('apis.html', {'request': request})
