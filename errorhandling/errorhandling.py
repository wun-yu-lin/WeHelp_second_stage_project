from flask import make_response
from werkzeug.exceptions import HTTPException

## Error handling
def handle_error(e):
    #error handling
    response_arg ={
        "headers": {
            "content-Type": "application/json"
        },
        "data": {
            "code": e["code"],
            "message": e["message"],
            "error": True
        }
    }
    #error handling
    response = make_response(response_arg, e["code"])
    return response