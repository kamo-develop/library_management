from fastapi import FastAPI
from auth import router as auth_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(auth_router)