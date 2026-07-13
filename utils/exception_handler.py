from fastapi import HTTPException


class ValidationException(HTTPException):

    def __init__(self, detail):

        super().__init__(
            status_code=400,
            detail=detail
        )


class NotFoundException(HTTPException):

    def __init__(self, detail):

        super().__init__(
            status_code=404,
            detail=detail
        )


class DatabaseException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=500,
            detail="Database Error"
        )