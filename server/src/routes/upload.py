from fastapi import APIRouter
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/upload", tags=["Upload PDF file"])
security = HTTPBearer()