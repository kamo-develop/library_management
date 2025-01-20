from fastapi import FastAPI
from user.user_routes import router as user_router
from book.book_routes import router as book_router
from book.author_routes import router as author_router
from book.borrowing_routes import router as borrowing_router
import logging
import uvicorn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(user_router)
app.include_router(book_router)
app.include_router(author_router)
app.include_router(borrowing_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
