import json

from fastapi import HTTPException


class APIException(HTTPException):

    err_code: str
    err_desc: str

    def __init__(
            self,
            status_code: int,
            err_code: str,
            err_desc: str
    ):
        self.err_code = err_code
        self.err_desc = err_desc

        super().__init__(
            status_code=status_code,
            detail=json.dumps({
                "err_code": err_code,
                "err_desc": err_desc
            })
        )

    def __str__(self):
        return f"err_code={self.err_code}, err_desc={self.err_desc}"
