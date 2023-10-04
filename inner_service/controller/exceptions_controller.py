from fastapi import HTTPException, status

NOT_FOUND = HTTPException(
    detail="Item not found",
    status_code=status.HTTP_404_NOT_FOUND
)

BAD_DATA = HTTPException(
    detail="Some values are invalided. Can be possible that some values have been stored",
    status_code=status.HTTP_400_BAD_REQUEST
)

GENERIC_DB_EXCEPTION = HTTPException(
    detail="Something went wrong with the data base",
    status_code=status.HTTP_400_BAD_REQUEST
)
