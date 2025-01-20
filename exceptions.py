from fastapi import HTTPException, status

BookNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found"
)

BookNotAvailableException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="There are no available copies of the book"
)

LimitBorrowingException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The number of borrowed books has exceeded the maximum limit"
)

BorrowingNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book borrowing not found"
)

AuthorNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Author not found"
)


UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found",
    headers={"WWW-Authenticate": "Bearer"},
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)

UnknownTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unknown token payload",
    headers={"WWW-Authenticate": "Bearer"},
)