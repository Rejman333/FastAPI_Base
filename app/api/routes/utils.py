from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/test-connection/",
    status_code=status.HTTP_200_OK,
)
def test_connection():
    """
    For testing if server is working
    """
    return {"status": "OK"}
