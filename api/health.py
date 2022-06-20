from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get('/health', status_code=status.HTTP_200_OK)
def health_check(response: Response):
    response.headers["X-Health-Check"] = "ok"
    return {
        'health': "ok"
    }

